from typing import List

from data_loader import DataLoader
from model import Issue

class Feature3:
    """
    Analyze a GitHub user's contribution quality.
    Flags as 'bad contributor' if:
    - They created more than 2 issues
    - And have less than 0.55 average comments per issue
    """

    def __init__(self):
        pass

    def run(self):
        username = input("Enter GitHub username to analyze: ").strip()
        self.analyze_contributor(username)

    def analyze_contributor(self, username: str):
        issues: List[Issue] = DataLoader().get_issues()

        issues_created = 0
        user_comments = 0

        for issue in issues:
            if issue.creator == username:
                issues_created += 1
            for event in issue.events:
                if event.event_type == "commented" and event.author == username:
                    user_comments += 1

        if issues_created == 0:
            print(f"\n❌ User '{username}' has not created any issues.")
            return

        avg_comment = user_comments / issues_created

        print(f"\n📊 Stats for '{username}':")
        print(f"- Issues Created: {issues_created}")
        print(f"- Comments Made: {user_comments}")
        print(f"- Avg Comments per Issue: {avg_comment:.2f}")

        if issues_created > 2 and avg_comment < 0.55:
            print("⚠️  Classification: BAD CONTRIBUTOR")
            print("📌 Reason: User creates many issues but rarely follows up.")
            print("📌 Recommendation to Maintainers: Consider prompting or deprioritizing this user's issues unless further engagement is shown.")
        else:
            print("✅ Classification: NOT a bad contributor")


if __name__ == '__main__':
    Feature3().run()
