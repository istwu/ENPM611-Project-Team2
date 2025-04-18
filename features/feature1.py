from typing import List
import matplotlib.pyplot as plt
import pandas as pd

from data_loader import DataLoader
from model import Issue

class Feature1:
    """
    Find what kinds of issues (eg. bugs, features) tend to have 
    the longest discussions (largest average number of comments)
    """

    def __init__(self):
        pass

    def run(self):
        ### BASIC STATISTICS
        # Store each issue's label and number of "comment" events
        issues:List[Issue] = DataLoader().get_issues()
        labels_comments = {"Labels":[], "Comments":[]}

        for i in issues:
            for l in i.labels:
                labels_comments["Labels"].append(l)
                labels_comments["Comments"].append(len(i.events))

        ### BAR CHART
        # Display a graph of the top 50 issue labels with the longest average
        # numbers of comments
        top_n:int = 50
        # Create a dataframe out of the labels_comments dict
        df = pd.DataFrame(labels_comments)
        # Calculate the average number of comments per label
        averages = df.groupby('Labels')['Comments'].mean()
        # Plot the chart
        averages.nlargest(top_n).plot(kind='bar', figsize=(14,8), title=f'Top {top_n} Issue Labels with the Largest Avg. Number of Comments', 
                                      xlabel='Label names', ylabel='Average # of Comments')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show() 


if __name__ == '__main__':
    # Invoke run method when running this module directly
    Feature1().run()