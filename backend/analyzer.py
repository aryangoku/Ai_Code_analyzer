import git
import uuid
import os
import re
import shutil
import subprocess
from radon.complexity import cc_visit
from github_data import get_repo_data, get_commit_activity, get_contributors, get_languages
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


def _clean_summary_text(text: str) -> str:
    """Best-effort cleanup of README snippet: drop HTML tags and markdown noise."""
    if not text:
        return ""
    # Remove HTML tags like <p>, <img>, etc.
    text = re.sub(r"<[^>]+>", " ", text)
    # Remove markdown image syntax: ![alt](url)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    # Replace markdown links [text](url) with just 'text'
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", lambda m: m.group(1), text)
    # Strip leading markdown headings/bullets
    text = re.sub(r"^[#>*\s]+\s*", "", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def analyze_repo(repo_url):
    folder = f"repo_{uuid.uuid4().hex}"
    try:
        git.Repo.clone_from(repo_url, folder, depth=1)
    except Exception as e:
        raise ValueError(f"Failed to clone repository: {e}") from e

    try:
        python_files: list[str] = []
        code_exts = (
            ".py",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".go",
            ".java",
            ".rb",
            ".php",
            ".cs",
            ".cpp",
            ".c",
            ".rs",
            ".kt",
            ".swift",
        )

        for root, dirs, files in os.walk(folder):
            for f in files:
                path = os.path.join(root, f)
                lower = f.lower()
                if lower.endswith(".py"):
                    python_files.append(path)

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

        commit_activity = get_commit_activity(repo_url)
        contributors = get_contributors(repo_url)
        languages_raw = get_languages(repo_url)
        dep_graph = build_dep_graph(folder)

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

        # Try to read README for a short, non-AI summary
        readme_text = ""
        for name in ("README.md", "Readme.md", "readme.md", "README.MD"):
            candidate = os.path.join(folder, name)
            if os.path.isfile(candidate):
                try:
                    with open(candidate, "r", errors="ignore") as f:
                        readme_text = f.read()
                except Exception:
                    readme_text = ""
                break

        # Simple repo summary from README (no AI) – prefer a real sentence over just the title
        repo_summary = None
        if readme_text:
            lines = [ln.strip() for ln in readme_text.splitlines()]
            paragraphs: list[list[str]] = []
            current: list[str] = []
            for ln in lines:
                if ln and not ln.lower().startswith("<img"):
                    current.append(ln)
                elif current:
                    paragraphs.append(current)
                    current = []
            if current:
                paragraphs.append(current)

            # Find the first paragraph that looks like a real description (not just the title)
            chosen = None
            for idx, para in enumerate(paragraphs):
                raw = " ".join(para)
                cleaned = _clean_summary_text(raw)
                if idx == 0 and len(cleaned.split()) <= 3:
                    # Very short first line (likely just project name) – skip it
                    continue
                if len(cleaned) >= 40 or any(ch in cleaned for ch in (".", ":", "–", "- ")):
                    chosen = cleaned
                    break

            if not chosen and paragraphs:
                chosen = _clean_summary_text(" ".join(paragraphs[0]))

            if chosen:
                repo_summary = chosen[:320]

        # Complexity hotspots: top Python files by average cyclomatic complexity and size
        hotspots = []
        for path in python_files:
            try:
                with open(path, "r", errors="ignore") as f:
                    code = f.read()
                loc = len(code.splitlines())
                results = cc_visit(code)
                if not results:
                    continue
                avg_file_complexity = sum(r.complexity for r in results) / len(results)
                score_hotspot = avg_file_complexity * (1 + loc / 200.0)
                rel_path = os.path.relpath(path, folder).replace("\\", "/")
                hotspots.append(
                    {
                        "path": rel_path,
                        "loc": loc,
                        "avg_complexity": round(avg_file_complexity, 2),
                        "functions": len(results),
                        "score": round(score_hotspot, 2),
                    }
                )
            except Exception:
                continue

        hotspots.sort(key=lambda h: h["score"], reverse=True)
        hotspots = hotspots[:10]

        # Repository quality checklist signals
        license_found = False
        ci_found = False
        tests_found = False

        for root, dirs, files in os.walk(folder):
            lower_files = [f.lower() for f in files]
            if any(fn in lower_files for fn in ("license", "license.md", "license.txt", "copying")):
                license_found = True
            if ".github" in dirs:
                workflows = os.path.join(root, ".github", "workflows")
                if os.path.isdir(workflows) and any(
                    name.endswith((".yml", ".yaml")) for name in os.listdir(workflows)
                ):
                    ci_found = True
            if any(d in ("tests", "test") for d in dirs):
                tests_found = True

        recent_active = False
        if commit_activity:
            for week in commit_activity[-12:]:
                if week.get("total", 0) > 0:
                    recent_active = True
                    break

        quality = {
            "readme": bool(readme_text),
            "license": license_found,
            "ci": ci_found,
            "tests": tests_found,
            "recent_activity": recent_active,
        }

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
            "languages": languages_raw,
            "dependency_graph": dep_graph,
            "engineering_health": engineering_health,
            "hotspots": hotspots,
            "repo_summary": repo_summary,
            "quality": quality,
        }

    finally:
        if os.path.isdir(folder):
            try:
                shutil.rmtree(folder, ignore_errors=True)
            except Exception:
                pass