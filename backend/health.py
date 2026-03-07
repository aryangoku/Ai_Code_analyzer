def compute_health(metrics):

    score = 100

    if metrics["avg_complexity"] > 10:
        score -= 30
    elif metrics["avg_complexity"] > 5:
        score -= 15

    if metrics["functions"] > 200:
        score -= 20

    if metrics["total_lines"] > 5000:
        score -= 20

    if metrics["file_count"] > 100:
        score -= 10

    return max(score,0)