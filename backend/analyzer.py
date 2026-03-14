import git
import uuid
import os
import re
import shutil
import subprocess
from radon.complexity import cc_visit
from github_data import get_repo_data, get_commit_activity, get_contributors, get_languages
from dependency_graph import build_graph as build_dep_graph
from ai_review import architecture_review, generate_recommendation, summarize_repo

TECH_STACK_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "React (JSX)",
    ".ts": "TypeScript",
    ".tsx": "React (TSX)",
    ".go": "Go",
    ".java": "Java",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".cpp": "C++",
    ".c": "C",
    ".rs": "Rust",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".dart": "Dart",
    ".lua": "Lua",
    ".r": "R",
    ".scala": "Scala",
    ".sh": "Shell",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".vue": "Vue",
    ".svelte": "Svelte",
}

FRAMEWORK_MARKERS = {
    "package.json": "Node.js",
    "requirements.txt": "Python (pip)",
    "Pipfile": "Python (pipenv)",
    "pyproject.toml": "Python (modern)",
    "Cargo.toml": "Rust (Cargo)",
    "go.mod": "Go Modules",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java (Gradle)",
    "Gemfile": "Ruby (Bundler)",
    "composer.json": "PHP (Composer)",
    "Dockerfile": "Docker",
    "docker-compose.yml": "Docker Compose",
    "docker-compose.yaml": "Docker Compose",
    ".github/workflows": "GitHub Actions",
    "Makefile": "Make",
    "CMakeLists.txt": "CMake",
    "tsconfig.json": "TypeScript",
    "tailwind.config.js": "Tailwind CSS",
    "next.config.js": "Next.js",
    "next.config.mjs": "Next.js",
    "nuxt.config.js": "Nuxt.js",
    "vite.config.js": "Vite",
    "vite.config.ts": "Vite",
    "webpack.config.js": "Webpack",
    "angular.json": "Angular",
    ".eslintrc.js": "ESLint",
    ".eslintrc.json": "ESLint",
    "jest.config.js": "Jest",
    "pytest.ini": "Pytest",
    "setup.py": "Python (setuptools)",
    ".flake8": "Flake8",
    ".prettierrc": "Prettier",
}


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
    """Rule-based fallback advice when Groq is unavailable."""
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
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", lambda m: m.group(1), text)
    text = re.sub(r"^[#>*\s]+\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _get_code_sample(folder: str, code_files: list[str]) -> str:
    """Collect a representative code sample for AI review."""
    sample_parts = []
    for path in code_files[:8]:
        try:
            with open(path, "r", errors="ignore") as f:
                content = f.read()
            if len(content) > 100:
                rel = os.path.relpath(path, folder).replace("\\", "/")
                snippet = content[:1500]
                sample_parts.append(f"--- {rel} ---\n{snippet}")
        except Exception:
            continue
    return "\n\n".join(sample_parts)


def _detect_tech_stack(folder: str) -> list[dict]:
    """Detect tech stack from file extensions and framework config files."""
    lang_counts: dict[str, int] = {}
    frameworks_found: set[str] = set()

    for root, dirs, files in os.walk(folder):
        if any(skip in root for skip in ("node_modules", ".git", "__pycache__", "venv")):
            continue
        for f in files:
            _, ext = os.path.splitext(f.lower())
            if ext in TECH_STACK_MAP:
                lang_counts[TECH_STACK_MAP[ext]] = lang_counts.get(TECH_STACK_MAP[ext], 0) + 1
            if f in FRAMEWORK_MARKERS:
                frameworks_found.add(FRAMEWORK_MARKERS[f])
        for d in dirs:
            path_key = os.path.join(d)
            if path_key in FRAMEWORK_MARKERS:
                frameworks_found.add(FRAMEWORK_MARKERS[path_key])

    stack = []
    for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1]):
        stack.append({"name": lang, "count": count, "type": "language"})
    for fw in sorted(frameworks_found):
        stack.append({"name": fw, "count": 0, "type": "framework"})

    return stack


def _calculate_bus_factor(contributors: list[dict]) -> dict:
    """Calculate bus factor: fewest people whose contributions total >= 50%."""
    if not contributors:
        return {"bus_factor": 0, "top_contributors": [], "total_contributions": 0}

    total = sum(c.get("contributions", 0) for c in contributors)
    if total == 0:
        return {"bus_factor": 0, "top_contributors": [], "total_contributions": 0}

    sorted_contribs = sorted(contributors, key=lambda c: c.get("contributions", 0), reverse=True)
    cumulative = 0
    bus_factor = 0
    top = []
    for c in sorted_contribs:
        cumulative += c.get("contributions", 0)
        bus_factor += 1
        pct = round(cumulative / total * 100, 1)
        top.append({
            "login": c.get("login", "unknown"),
            "contributions": c.get("contributions", 0),
            "cumulative_pct": pct,
        })
        if cumulative >= total * 0.5:
            break

    return {
        "bus_factor": bus_factor,
        "top_contributors": top,
        "total_contributions": total,
    }


def analyze_repo(repo_url):
    folder = f"repo_{uuid.uuid4().hex}"
    try:
        git.Repo.clone_from(repo_url, folder, depth=1)
    except Exception as e:
        raise ValueError(f"Failed to clone repository: {e}") from e

    try:
        python_files: list[str] = []
        code_files: list[str] = []
        code_exts = (
            ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".java", ".rb",
            ".php", ".cs", ".cpp", ".c", ".rs", ".kt", ".swift",
        )

        for root, dirs, files in os.walk(folder):
            if any(skip in root for skip in ("node_modules", ".git", "__pycache__", "venv")):
                continue
            for f in files:
                path = os.path.join(root, f)
                lower = f.lower()
                if lower.endswith(".py"):
                    python_files.append(path)
                if any(lower.endswith(ext) for ext in code_exts):
                    code_files.append(path)

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
        total_files = len(code_files)
        large_files = sum(1 for f in code_files if os.path.getsize(f) > 50000)

        try:
            security = subprocess.getoutput(f"python -m bandit -r {folder} 2>&1")
        except Exception:
            security = "Security scan could not be run."

        github = get_repo_data(repo_url)
        score = max(0, 100 - avg_complexity * 3)
        risk = calculate_risk(avg_complexity, github["issues"], large_files)
        repo_name = repo_url.rstrip("/").split("/")[-1] or "repository"
        language = github.get("language") or "Python"

        commit_activity = get_commit_activity(repo_url)
        contributors = get_contributors(repo_url)
        languages_raw = get_languages(repo_url)
        dep_graph = build_dep_graph(folder)
        tech_stack = _detect_tech_stack(folder)
        bus_factor_data = _calculate_bus_factor(contributors)

        # AI-powered recommendation via Groq (falls back to rule-based)
        ai_rec = generate_recommendation(repo_name, language, score, avg_complexity, total_files)
        advice = ai_rec or generate_ai_advice(score, avg_complexity, repo_name, language, total_files)

        # AI architecture review via Groq
        code_sample = _get_code_sample(folder, code_files)
        ai_review = architecture_review(code_sample, repo_name, language)

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

        # Read README for summary
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

        # AI-powered summary via Groq (falls back to README extraction)
        ai_summary = summarize_repo(readme_text, repo_name)
        if ai_summary:
            repo_summary = ai_summary
        else:
            repo_summary = _extract_readme_summary(readme_text)

        # Complexity hotspots
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
                hotspots.append({
                    "path": rel_path,
                    "loc": loc,
                    "avg_complexity": round(avg_file_complexity, 2),
                    "functions": len(results),
                    "score": round(score_hotspot, 2),
                })
            except Exception:
                continue

        hotspots.sort(key=lambda h: h["score"], reverse=True)
        hotspots = hotspots[:10]

        # Quality checklist
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
            "ai_review": ai_review,
            "security_report": (security or "")[:1200],
            "commit_activity": commit_activity,
            "contributors": contributors,
            "languages": languages_raw,
            "dependency_graph": dep_graph,
            "engineering_health": engineering_health,
            "hotspots": hotspots,
            "repo_summary": repo_summary,
            "quality": quality,
            "tech_stack": tech_stack,
            "bus_factor": bus_factor_data,
        }

    finally:
        if os.path.isdir(folder):
            try:
                shutil.rmtree(folder, ignore_errors=True)
            except Exception:
                pass


def _extract_readme_summary(readme_text: str) -> str | None:
    """Fallback: extract summary from README without AI."""
    if not readme_text:
        return None

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

    chosen = None
    for idx, para in enumerate(paragraphs):
        raw = " ".join(para)
        cleaned = _clean_summary_text(raw)
        if idx == 0 and len(cleaned.split()) <= 3:
            continue
        if len(cleaned) >= 40 or any(ch in cleaned for ch in (".", ":", "\u2013", "- ")):
            chosen = cleaned
            break

    if not chosen and paragraphs:
        chosen = _clean_summary_text(" ".join(paragraphs[0]))

    return chosen[:320] if chosen else None
