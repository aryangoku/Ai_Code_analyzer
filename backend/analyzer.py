import git
import uuid
import os
import subprocess
from radon.complexity import cc_visit
from github_data import get_repo_data


def calculate_risk(complexity, issues, large_files):

    risk = 0

    if complexity > 15:
        risk += 30
    elif complexity > 10:
        risk += 15

    if issues > 200:
        risk += 25

    if large_files > 5:
        risk += 20

    return min(risk,100)


def generate_ai_advice(score, complexity):

    if score > 80:
        return "Repository structure is healthy with manageable complexity."

    if complexity > 15:
        return "High complexity detected. Consider breaking large functions."

    return "Moderate code health. Refactoring and better test coverage recommended."


def analyze_repo(repo_url):

    folder = f"repo_{uuid.uuid4().hex}"

    git.Repo.clone_from(repo_url, folder)

    python_files = []

    for root,dirs,files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                python_files.append(os.path.join(root,f))

    complexities=[]

    for file in python_files:

        with open(file,"r",errors="ignore") as f:
            code=f.read()

        results=cc_visit(code)

        for r in results:
            complexities.append(r.complexity)

    avg_complexity = sum(complexities)/len(complexities) if complexities else 0

    total_files=len(python_files)

    large_files=sum(
        1 for f in python_files if os.path.getsize(f)>50000
    )

    security = subprocess.getoutput(f"python -m bandit -r {folder}")

    github = get_repo_data(repo_url)

    score=max(0,100-avg_complexity*3)

    risk=calculate_risk(avg_complexity, github["issues"], large_files)

    advice=generate_ai_advice(score, avg_complexity)

    return {

        "health_score":round(score,2),

        "complexity":round(avg_complexity,2),

        "stars":github["stars"],
        "forks":github["forks"],
        "language":github["language"],
        "issues":github["issues"],

        "total_files":total_files,
        "large_files":large_files,

        "risk_score":risk,

        "ai_recommendation":advice,

        "security_report":security[:800]

    }