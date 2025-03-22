import requests, json
global username, token

def fetch_issue_timeline(number):
    url = f"https://api.github.com/repos/python-poetry/poetry/issues/{number}/timeline"
    response = requests.get(url, auth=(username, token))
    result = []

    events = response.json()
    for event in events:
        if event.get("event") == "labeled":
            result.append({
                "event_type": event.get("event"),
                "author": event.get("actor", {}).get("login"),
                "event_date": event.get("created_at"),
                "label": event.get("label", {}).get("name")
            })
        elif event.get("event") == "commented":
            result.append({
                "event_type": event.get("event"),
                "author": event.get("actor", {}).get("login"),
                "event_date": event.get("created_at"),
                "comment": event.get("body")
            })
        else:
            result.append({
                "event_type": event.get("event"),
                "author": event.get("actor", {}).get("login"),
                "event_date": event.get("created_at")
            })

    return result


def format_issue(issue):
    return {
        "url": issue.get("html_url"),
        "creator": issue.get("user", {}).get("login"),
        "labels": [label["name"] for label in issue.get("labels", [])],
        "state": issue.get("state"),
        "assignees": [assignee["login"] for assignee in issue.get("assignees", [])],
        "title": issue.get("title"),
        "text": issue.get("body", "").replace("\r", ""),    # Preserving newlines and formatting
        "number": issue.get("number"),
        "created_date": issue.get("created_at"),
        "updated_date": issue.get("updated_at"),
        "timeline_url": f"http://api.github.com/repos/python-poetry/poetry/issues/{issue.get('number')}/timeline",
        "events": fetch_issue_timeline(issue.get("number"))
    }


if __name__ == '__main__':
    username = input("Enter GitHub username: ")
    token = input("Enter GitHub API token: ")
    url = f"https://api.github.com/repos/python-poetry/poetry/issues"
    response = requests.get(url, auth=(username, token))

    if response.status_code == 200:
        with open("poetry.json", "w") as file:
            issues = response.json()
            for issue in issues:
                json.dump(format_issue(issue), file, indent=4)
    else:
        print(f"Error: {response.status_code}, {response.text}")