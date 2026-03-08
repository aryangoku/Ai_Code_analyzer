import git
import uuid
import os
import shutil
import subprocess
from radon.complexity import cc_visit
from github_data import get_repo_data, get_commit_activity, get_contributors
from dependency_graph import build_graph as build_dep_graph


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
    return min(risk, 100)


def generate_ai_advice(score, complexity, repo_name="", language="Python", total_files=0):
    """Rule-based advice with repo-specific details so it varies per repo."""
    name = repo_name or "This repository"
    lang = language or "Python"
    if score > 80:
        return f"{name} ({lang}, {total_files} files) is in good shape with manageable complexity. Keep tests and docs in sync as it grows."
    if complexity > 15:
        return f"High cyclomatic complexity in {name}. Consider splitting large functions and adding unit tests for critical paths."
    if total_files > 50:
        return f"{name} has moderate health with many files ({total_files}). Focus on refactoring hotspots and improving test coverage."
    return f"Moderate code health for {name}. Refactoring complex modules and adding tests will improve maintainability."


def _get_code_sample(python_files, max_chars=4000):
    """Build a small code sample for AI review from first few files."""
    sample = []
    total = 0
    for path in python_files[:5]:
        if total >= max_chars:
            break
        try:
            with open(path, "r", errors="ignore") as f:
                content = f.read()
            chunk = content[: max_chars - total]
            sample.append(f"# {path}\n{chunk}")
            total += len(chunk)
        except Exception:
            continue
    return "\n\n".join(sample) if sample else ""


def analyze_repo(repo_url):
    folder = f"repo_{uuid.uuid4().hex}"
    try:
        git.Repo.clone_from(repo_url, folder, depth=1)
    except Exception as e:
        raise ValueError(f"Failed to clone repository: {e}") from e

    try:
        python_files = []
        for root, dirs, files in os.walk(folder):
            for f in files:
                if f.endswith(".py"):
                    python_files.append(os.path.join(root, f))

        complexities = []
        for file in python_files:
            try:
                with open(file, "r", errors="ignore") as f:
                    code = f.read()
                results = cc_visit(code)
                for r in results:
                    complexities.append(r.complexity)
            except Exception:
                continue

        avg_complexity = sum(complexities) / len(complexities) if complexities else 0
        total_files = len(python_files)
        large_files = sum(1 for f in python_files if os.path.getsize(f) > 50000)

        try:
            security = subprocess.getoutput(f"python -m bandit -r {folder} 2>&1")
        except Exception:
            security = "Security scan could not be run."

        github = get_repo_data(repo_url)
        score = max(0, 100 - avg_complexity * 3)
        risk = calculate_risk(avg_complexity, github["issues"], large_files)
        repo_name = repo_url.rstrip("/").split("/")[-1] or "repository"
        language = github.get("language") or "Python"
        advice = generate_ai_advice(score, avg_complexity, repo_name, language, total_files)

        # Commit heatmap + contributors (real GitHub data)
        commit_activity = get_commit_activity(repo_url)
        contributors = get_contributors(repo_url)

        # Dependency graph from cloned repo
        dep_graph = build_dep_graph(folder)

        # Engineering health breakdown (0–100 per dimension)
        activity_score = min(100, (github["stars"] or 0) // 2 + (github["forks"] or 0) * 5 + 20)
        security_issues = "High" in (security or "") or "Medium" in (security or "")
        security_score = 20 if security_issues else 100
        engineering_health = {
            "overall": round(score, 2),
            "complexity_score": max(0, min(100, 100 - avg_complexity * 5)),
            "risk_score": max(0, 100 - risk),
            "security_score": security_score,
            "activity_score": activity_score,
        }

        # Full AI architecture review + unique recommendation (repo-specific)
        code_sample = _get_code_sample(python_files)
        ai_architecture_review = None
        if os.getenv("OPENAI_API_KEY"):
            try:
                from ai_review import architecture_review, generate_recommendation
                if code_sample:
                    ai_architecture_review = architecture_review(
                        code_sample, repo_name=repo_name, language=language
                    )
                    advice = generate_recommendation(
                        code_sample, repo_name, language,
                        score, avg_complexity, total_files, risk,
                    )
            except Exception:
                pass

        return {
            "repo_name": repo_name,
            "repo_url": repo_url,
            "health_score": round(score, 2),
            "complexity": round(avg_complexity, 2),
            "stars": github["stars"],
            "forks": github["forks"],
            "language": github["language"],
            "issues": github["issues"],
            "total_files": total_files,
            "large_files": large_files,
            "risk_score": risk,
            "ai_recommendation": advice,
            "security_report": (security or "")[:1200],
            "commit_activity": commit_activity,
            "contributors": contributors,
            "dependency_graph": dep_graph,
            "engineering_health": engineering_health,
            "ai_architecture_review": ai_architecture_review,
        }
    finally:
        if os.path.isdir(folder):
            try:
                shutil.rmtree(folder, ignore_errors=True)
            except Exception:
                pass