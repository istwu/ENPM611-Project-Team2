from typing import List
import matplotlib.pyplot as plt
import pandas as pd

from data_loader import DataLoader
from model import Issue

from collections import defaultdict
from datetime import datetime

class Feature1:
    def run(self):
        # Get issues
        issues: List[Issue] = DataLoader().get_issues()

        # Initial dictionary (Issue number and it's asscociated label(s), number of events, comments, and duration)
        data = {
            "issue_number": [],
            "label": [],
            "num_events": [],
            "num_comments": [],
            "duration_sec": [],
        }

        # Populate the dictionary
        for issue in issues:
            if not issue.events:
                continue

            for label in issue.labels:
                events = issue.events
                num_comments = sum(1 for e in events if e.event_type == "commented")
                times = [e.event_date for e in events if e.event_date]
                duration = (max(times) - min(times)).total_seconds() if len(times) >= 2 else 0
                
                data["issue_number"].append(issue.number)
                data["label"].append(label)
                data["num_events"].append(len(events))
                data["num_comments"].append(num_comments)
                data["duration_sec"].append(duration)

        # Create the initial dataframe from initial data (dictionary)
        df = pd.DataFrame(data)

        # Aggregate statistics per label (total issues, average events, comments, durations)
        summary = df.groupby("label").agg({
            "issue_number": "count",
            "num_events": "mean",
            "num_comments": "mean",
            "duration_sec": "mean"
        }).rename(columns={
            "issue_number": "total_issues",
            "num_events": "avg_events",
            "num_comments": "avg_comments",
            "duration_sec": "avg_duration_sec"
        })

        # Filter out labels that have very few issues associated with it (lower than the median number of issuer per label, which is 30)
        summary = summary[summary["total_issues"] >= 30]

        # More statistics (avg comment per avg events and average duration in hours)
        summary["comment_event_ratio"] = summary["avg_comments"] / summary["avg_events"]
        summary["avg_duration_hr"] = summary["avg_duration_sec"] / 3600

        # Further filter to exclude labels with avg_duration_hr below the mean
        mean_duration_hr = summary["avg_duration_hr"].mean()
        print("Mean duration (in hours):", mean_duration_hr)
        summary = summary[
            (summary["avg_duration_hr"] >= mean_duration_hr)
        ]
        

        # Filters/sorts problematic events (average duration is greater than a day and comment event ratio is less than mean) and 
        # lists only the 10 (at maximum) worst 
        mean_comment_event_ratio = summary["comment_event_ratio"].mean()
        print("Mean comment event ratio", mean_comment_event_ratio)
        slow_low_engagement = summary[(summary["comment_event_ratio"] < mean_comment_event_ratio)].sort_values("avg_duration_hr", ascending=False).head(10)

        # Print the problematic issues
        print("🚩 Labels (at most 10) with slow response and low interaction:")
        print(slow_low_engagement[["avg_duration_hr", "comment_event_ratio", "total_issues"]])

        # Top levels according to comment_event ratio
        top_labels = summary[(summary["comment_event_ratio"] >= mean_comment_event_ratio)]["comment_event_ratio"].nlargest(30)

        # Print duration and issue count for the top 30 labels
        print("\n\U0001F3C6 Top 30 (at maximum) Labels by Comment-to-Event Ratio:")
        print(summary.loc[top_labels.index, ["avg_duration_hr", "total_issues"]])

        # Plot the top 30 labels with highest comment-to-event ratio (i.e., good engagement)
        top_labels.plot(
            kind='bar', figsize=(14, 6),
            title="Labels with Highest Comment-to-Event Ratio"
        )
        plt.ylabel("Comment-to-Event Ratio")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        

if __name__ == '__main__':
    # Invoke run method when running this module directly
    Feature1().run()