import requests, json
from typing import List
from data_loader import DataLoader
from model import Issue, Event
import scraper

def analyze_data() :
    issues:List[Issue] = DataLoader().get_issues()
    events = []
    creators, states, issue_labels, event_types, authors, event_labels = set(), set(), set(), set(), set(), set()
    for i in issues:
        events.extend(i.events)
        creators.add(i.creator)
        states.add(i.state)
        issue_labels.update(i.labels)
    for e in events:
        event_types.add(e.event_type)
        if e.author:
            authors.add(e.author)
        if e.label:
            event_labels.add(e.label)

    # =====  Print the number of issues, events, and so on  ==== #
    print("# of issues:", len(issues))
    print("# of events:", len(events))
    print("# of issue creators:", len(creators))
    print("# of states:", len(states))
    print("# of issue labels:", len(issue_labels))
    print("# of event types:", len(event_types))
    print("# of event authors:", len(authors))
    print("# of event labels:", len(event_labels))

    # ==== Write data to text files ==== #

    # Write issue creators
    with open("text_files/issue_creators.txt", "w", encoding="utf-8") as f:
        for creator in sorted(creators):
            f.write(creator + "\n")

    # Write states
    with open("text_files/states.txt", "w", encoding="utf-8") as f:
        for state in sorted(states):
            f.write(state + "\n")

    # Write issue labels
    with open("text_files/issue_labels.txt", "w", encoding="utf-8") as f:
        for label in sorted(issue_labels):
            f.write(label + "\n")

    # Write event types
    with open("text_files/event_types.txt", "w", encoding="utf-8") as f:
        for event_type in sorted(event_types):
            f.write(event_type + "\n")

    # Write event authors
    with open("text_files/event_authors.txt", "w", encoding="utf-8") as f:
        for author in sorted(authors):
            f.write(author + "\n")

        # Write event labels
    with open("text_files/event_labels.txt", "w", encoding="utf-8") as f:
        for label in sorted(event_labels):
            f.write(label + "\n")


# ==== Identiy bot accounts that have authored events ==== #
def get_bot_authors(token):
    bots = []
    
    with open("text_files/event_authors.txt", "r") as file:
        for author in file:
            author = author.strip()
            url = f'https://api.github.com/users/{author}'

            scraper.check_rate_limit()
            response = requests.get(url, headers={"Authorization": f"token {token}"})

            if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
                print(url)
                continue

            author_info = response.json()
            if not author_info:
                continue

            if author_info.get("type") == "Bot":
                bots.append(author)

        # Write to bot_authors.txt
        with open("text_files/event_authors_bots.txt", "w", encoding="utf-8") as f:
            for bot in sorted(bots):
                f.write(bot + "\n")


if __name__ == '__main__':
    analyze_data()

    # scraper.token = input("Enter GitHub API token: ")
    # remove_orgs(scraper.token)