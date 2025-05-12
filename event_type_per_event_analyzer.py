from typing import List
import pandas as pd
from data_loader import DataLoader
from model import Issue, Event

def calculate_events_per_event_type():
    # Load all issues and extract events
    issues: List[Issue] = DataLoader().get_issues()
    events: List[Event] = [event for issue in issues for event in issue.events]

    # Count the number of events per event_type
    event_type_counts = {}

    for event in events:
        if event.event_type:
            if event.event_type in event_type_counts:
                event_type_counts[event.event_type] += 1
            else:
                event_type_counts[event.event_type] = 1

    # Convert to DataFrame
    df = pd.DataFrame(list(event_type_counts.items()), columns=["EventType", "EventCount"])

    # Print basic stats
    print("\n🔢 Basic statistics on event type usage:")
    print(df["EventCount"].describe())

    # Print top 10 event types
    print("\n🏆 Top 10 Event Types by Number of Events:")
    print(df.sort_values("EventCount", ascending=False).head(10))

if __name__ == '__main__':
    calculate_events_per_event_type()