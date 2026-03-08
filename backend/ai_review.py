from openai import OpenAI

client = OpenAI()


def architecture_review(code_sample: str, repo_name: str = "", language: str = "Python") -> str:
    """Generate a unique architecture review for this specific repository."""
    repo_context = f"Repository: {repo_name}" if repo_name else "Repository (unknown)"
    prompt = f"""You are a senior software architect. Analyze ONLY this specific codebase and give concrete, repo-specific advice.

{repo_context}
Primary language: {language}

Below is a code sample from this repository. Analyze its structure, patterns, and potential issues. Give 3-5 specific, actionable suggestions for THIS codebase. Do not give generic advice—reference what you see in the code. Be concise.

Code sample:
```
{code_sample[:6000]}
```

Your analysis (repo-specific):"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return (res.choices[0].message.content or "").strip()


def generate_recommendation(
    code_sample: str,
    repo_name: str,
    language: str,
    health_score: float,
    complexity: float,
    total_files: int,
    risk_score: int,
) -> str:
    """Generate a unique short AI recommendation for this repo based on its metrics and code."""
    prompt = f"""You are a code quality advisor. In 2-4 short sentences, give a specific recommendation for THIS repository only. Use the metrics and code context below. Do not repeat generic phrases—reference the repo name or its characteristics.

Repo: {repo_name}
Language: {language}
Health score: {health_score}/100 | Avg complexity: {complexity} | Python files: {total_files} | Risk: {risk_score}/100

Code snippet (for context):
```
{code_sample[:2500]}
```

Brief, specific recommendation for this repo:"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )
    return (res.choices[0].message.content or "").strip()
