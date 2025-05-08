from typing import List
import matplotlib.pyplot as plt
import pandas as pd

from data_loader import DataLoader
from model import Issue

class Feature1:
    """
    Find what kinds of issues (eg. bugs, features) tend to have 
    the most user interaction (largest average number of events)
    """

    def __init__(self):
        pass

    def run(self):
        ### BASIC STATISTICS
        # Store each issue's label and number of events
        issues:List[Issue] = DataLoader().get_issues()
        labels_events = {"Labels":[], "Events":[]}

        for i in issues:
            for l in i.labels:
                labels_events["Labels"].append(l)
                labels_events["Events"].append(len(i.events))

        ### BAR CHART
        # Display a graph of the top 50 issue labels with the largest avg
        # numbers of events
        top_n:int = 50
        # Create a dataframe out of the labels_events dict
        df = pd.DataFrame(labels_events)
        # Calculate the average number of evnets per label
        averages = df.groupby('Labels')['Events'].mean()
        # Plot the chart
        averages.nlargest(top_n).plot(kind='bar', figsize=(14,8), title=f'Top {top_n} Issue Labels with the Largest Avg. Number of Events', 
                                      xlabel='Label names', ylabel='Average # of Events')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show() 


if __name__ == '__main__':
    # Invoke run method when running this module directly
    Feature1().run()