import requests

def get_repo_data(repo_url):

    try:

        repo_path = repo_url.replace("https://github.com/", "").strip("/")

        parts = repo_path.split("/")

        if len(parts) < 2:
            return {
                "stars":0,
                "forks":0,
                "language":"Unknown",
                "issues":0
            }

        owner = parts[0]
        repo = parts[1]

        api = f"https://api.github.com/repos/{owner}/{repo}"

        r = requests.get(api)

        data = r.json()

        if "message" in data:
            return {
                "stars":0,
                "forks":0,
                "language":"Unknown",
                "issues":0
            }

        return {
            "stars": data.get("stargazers_count",0),
            "forks": data.get("forks_count",0),
            "language": data.get("language","Unknown"),
            "issues": data.get("open_issues_count",0)
        }

    except:
        return {
            "stars":0,
            "forks":0,
            "language":"Unknown",
            "issues":0
        }