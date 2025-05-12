from typing import List, Dict
from collections import defaultdict
import statistics

from data_loader import DataLoader
from model import Issue



def analyze_author():
    issues: List[Issue] = DataLoader().get_issues()

    issue_counts: Dict[str, int] = defaultdict(int)
    comment_counts: Dict[str, int] = defaultdict(int)
    event_counts: Dict[str, int] = defaultdict(int)

    for issue in issues:
        creator = issue.creator
        issue_counts[creator] += 1
        for event in issue.events:
            if event.author:
                event_counts[event.author] += 1
                if event.event_type == "commented":
                    comment_counts[event.author] += 1

    # Calculate comment-to-event ratios per user
    comment_ratios = []
    for user in event_counts:
        if event_counts[user] > 0:
            ratio = comment_counts[user] / event_counts[user]
            comment_ratios.append(ratio)

    # Median values
    issue_median = statistics.mean(issue_counts.values()) if issue_counts else 0
    comment_ratio_median = statistics.mean(comment_ratios) if comment_ratios else 0

    print("\n📊 Author Behavior Summary:")
    print(f"🟡 Mean number of issues created per user: {issue_median}")
    print(f"🟣 Mean comment-to-event ratio per user: {comment_ratio_median:.2f}")

if __name__ == '__main__':
    analyze_author()
