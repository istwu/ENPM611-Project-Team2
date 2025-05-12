from typing import List
import pandas as pd
from data_loader import DataLoader
from model import Issue

def calculate_average_issues_per_label():
    # Load issues
    issues: List[Issue] = DataLoader().get_issues()

    # Create a dictionary to store label -> number of times it appears (once per issue)
    label_issue_counts = {}

    for issue in issues:
        for label in issue.labels:
            if label in label_issue_counts:
                label_issue_counts[label] += 1
            else:
                label_issue_counts[label] = 1

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(list(label_issue_counts.items()), columns=["Label", "IssueCount"])

    # Basic stats
    print("\n🔢 Basic statistics:")
    print(df["IssueCount"].describe())

if __name__ == '__main__':
    calculate_average_issues_per_label()