def detect_risks(metrics):

    risks = []

    if metrics["avg_complexity"] > 10:
        risks.append("High cyclomatic complexity")

    if metrics["total_lines"] > 5000:
        risks.append("Large codebase maintainability risk")

    if metrics["functions"] > 200:
        risks.append("Too many functions")

    if not risks:
        risks.append("Low risk codebase")

    return risks