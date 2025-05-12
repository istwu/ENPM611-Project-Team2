from typing import List
import matplotlib.pyplot as plt
import pandas as pd

from data_loader import DataLoader
from model import Issue



def bot_analzye():
    ### LOAD BOT USERNAMES ###
    with open("text_files/event_authors_bots.txt", "r", encoding="utf-8") as f:
        bot_usernames = set(line.strip() for line in f)

    ### LOAD ISSUES ###
    issues: List[Issue] = DataLoader().get_issues()
    bot_event_counts = {}

    for issue in issues:
        for event in issue.events:
            if event.author in bot_usernames:
                bot_event_counts[event.author] = bot_event_counts.get(event.author, 0) + 1

    ### BAR CHART ###
    # Convert to DataFrame
    df = pd.DataFrame(list(bot_event_counts.items()), columns=["Bot", "Event Count"])
    df = df.sort_values(by="Event Count", ascending=False)

    # Plot
    plt.figure(figsize=(14, 8))
    bars = plt.bar(df["Bot"], df["Event Count"])
    plt.title("Bot Engagement: Number of Events by Each Bot")
    plt.xlabel("Bot Username")
    plt.ylabel("Number of Events Authored")
    plt.xticks(rotation=45, ha='right')

    # Add text labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 100, f'{int(height)}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    bot_analzye()
