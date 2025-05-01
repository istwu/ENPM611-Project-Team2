import unittest
from unittest.mock import patch, mock_open, MagicMock
from features.feature2 import Feature2  # <-- updated import path
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend


class TestFeature2(unittest.TestCase):
    
    @patch("builtins.open", new_callable=mock_open, read_data="github-actions[bot]\nauto-bot\n")
    @patch("features.feature2.DataLoader")  # <-- updated patch path
    def test_bot_event_counts(self, mock_data_loader, mock_file):
        # Create mock events
        mock_event1 = MagicMock(author="github-actions[bot]")
        mock_event2 = MagicMock(author="auto-bot")
        mock_event3 = MagicMock(author="random-human")
        mock_event4 = MagicMock(author="github-actions[bot]")

        # Mock issue
        mock_issue = MagicMock()
        mock_issue.events = [mock_event1, mock_event2, mock_event3, mock_event4]

        mock_data_loader.return_value.get_issues.return_value = [mock_issue]

        feature = Feature2()

        # Suppress chart
        with patch("matplotlib.pyplot.show"):
            feature.run()

        mock_file.assert_called_once_with("text_files/event_authors_bots.txt", "r", encoding="utf-8")
        mock_data_loader.return_value.get_issues.assert_called_once()

if __name__ == '__main__':
    unittest.main()
