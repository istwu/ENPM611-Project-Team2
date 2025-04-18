from typing import List

from data_loader import DataLoader
from model import Issue

class Feature3:
    """
    Analyze GitHub issues and events to determine the number of issues and 
    comments/events created by a specific user.
    """

    def __init__(self):
        pass

    def run(self):
        # Prompt for username input
        username = input("Enter GitHub username: ").strip()
        self.count_issues_and_events_by_user(username)

    def count_issues_and_events_by_user(self, username: str):
        issues: List[Issue] = DataLoader().get_issues()
        
        issue_count = 0
        event_count = 0
        
        for issue in issues:
            if issue.creator == username:
                issue_count += 1
            for event in issue.events:
                if hasattr(event, 'author') and event.author == username:
                    event_count += 1
        
        print(f"{username} has created {issue_count} issues and {event_count} issue comments/events.")


if __name__ == '__main__':
    Feature3().run()
