import requests

def get_repo_info(repo_url):

    repo = repo_url.replace("https://github.com/","")

    url = f"https://api.github.com/repos/{repo}"

    res = requests.get(url).json()

    return {
        "stars": res.get("stargazers_count",0),
        "forks": res.get("forks_count",0),
        "issues": res.get("open_issues_count",0),
        "language": res.get("language","Unknown")
    }