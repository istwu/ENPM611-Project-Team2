from typing import List
import matplotlib.pyplot as plt
import pandas as pd

from data_loader import DataLoader
from model import Issue

class Feature2:
    """
    Compare event type breakdown for github-actions[bot] and stale[bot].
    """

    def __init__(self):
        self.bots = ["github-actions[bot]", "stale[bot]"]

    def run(self):
        ### LOAD ISSUES ###
        issues: List[Issue] = DataLoader().get_issues()

        # Count event types for each bot
        bot_event_type_counts = {bot: {} for bot in self.bots}

        for issue in issues:
            for event in issue.events:
                if event.author in self.bots:
                    event_type = event.event_type or "unknown"
                    current_bot = event.author
                    bot_event_type_counts[current_bot][event_type] = (
                        bot_event_type_counts[current_bot].get(event_type, 0) + 1
                    )

        ### PLOTTING ###
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))

        for i, bot in enumerate(self.bots):
            data = bot_event_type_counts[bot]
            df = pd.DataFrame(list(data.items()), columns=["Event Type", "Count"])
            df = df.sort_values(by="Count", ascending=False)

            bars = axes[i].bar(df["Event Type"], df["Count"])
            axes[i].set_title(f"Actions of {bot}: Event Type Breakdown")
            axes[i].set_xlabel("Event Type")
            axes[i].set_ylabel("Number of Events")
            axes[i].tick_params(axis='x', rotation=45)

            # Add text labels on bars
            for bar in bars:
                height = bar.get_height()
                axes[i].text(bar.get_x() + bar.get_width()/2., height + 5,
                             f'{int(height)}', ha='center', va='bottom')

        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    Feature2().run()
