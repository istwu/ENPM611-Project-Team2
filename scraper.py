import requests, time, json

global token

def check_rate_limit():
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers={"Authorization": f"token {token}"})

    if response.status_code == 200:
        data = response.json()
        remaining = data["rate"]["remaining"]
        reset_time = data["rate"]["reset"]
        
        if remaining == 0:
            wait_time = reset_time - int(time.time())
            print(f"Rate limit reached, waiting {wait_time} seconds until reset")
            time.sleep(wait_time + 1)
            print("Continuing")


def fetch_issue_timeline(number):
    url = f"https://api.github.com/repos/python-poetry/poetry/issues/{number}/timeline"
    result = []

    while url:
        check_rate_limit()
        response = requests.get(url, headers={"Authorization": f"token {token}"})
        
        if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
                break
        
        events = response.json()
        if not events: 
            break
        
        for event in events:
            event_data = {
                "event_type": event.get("event"),
                "author": event.get("actor", {}).get("login") if event.get("actor", {}) else None,
                "event_date": event.get("created_at")
            }

            if event.get("event") == "labeled":
                event_data["label"] = event.get("label", {}).get("name")
            elif event.get("event") == "commented":
                event_data["comment"] = event.get("body")

            result.append(event_data)
        
        url = None
        if "Link" in response.headers:
            links = response.headers["Link"].split(", ")
            for link in links:
                if 'rel="next"' in link:
                    url = link.split(";")[0].strip("<>")

    return result


def format_issue(issue):
    return {
        "url": issue.get("html_url"),
        "creator": issue.get("user", {}).get("login"),
        "labels": [label["name"] for label in issue.get("labels", [])],
        "state": issue.get("state"),
        "assignees": [assignee["login"] for assignee in issue.get("assignees", [])],
        "title": issue.get("title"),
        "text": issue.get("body", "").replace("\r", "") if issue.get("body", "") else None,    # Preserving newlines and formatting
        "number": issue.get("number"),
        "created_date": issue.get("created_at"),
        "updated_date": issue.get("updated_at"),
        "timeline_url": f"https://api.github.com/repos/python-poetry/poetry/issues/{issue.get('number')}/timeline",
        "events": fetch_issue_timeline(issue.get("number"))
    }


def fetch_all_issues():
    url = f"https://api.github.com/repos/python-poetry/poetry/issues"
    params = {
        "state": "all",
        "per_page": 100,
    }
    result = []

    while url:
        check_rate_limit()
        response = requests.get(url, headers={"Authorization": f"token {token}"}, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break

        issues = response.json()
        if not issues: 
            break

        for issue in issues:
            print(issue.get("number"))
            result.append(format_issue(issue))

        url = None
        if "Link" in response.headers:
            links = response.headers["Link"].split(", ")
            for link in links:
                if 'rel="next"' in link:
                    url = link.split(";")[0].strip("<>")
    
    return result


if __name__ == '__main__':
    token = input("Enter GitHub API token: ")

    result = fetch_all_issues()
        
    print("Issues fetched: ", len(result))
    with open("poetry.json", "w") as file:
        json.dump(result, file, indent=4)