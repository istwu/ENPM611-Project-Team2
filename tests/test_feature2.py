# tests/test_feature2.py (final fix for headless test environments)
import unittest
from unittest.mock import patch, mock_open, MagicMock
import matplotlib
matplotlib.use("Agg")  # <-- force headless backend for matplotlib

from features.feature2 import Feature2
from model import Issue

class TestFeature2(unittest.TestCase):

    def setUp(self):
        self.sample_issues = [
            Issue({"state": "open", "events": [
                {"author": "user1"},
                {"author": "github-actions[bot]"},
                {"author": "github-actions[bot]"},
            ]}),
            Issue({"state": "open", "events": [
                {"author": "dependabot[bot]"},
                {"author": "user2"},
            ]}),
            Issue({"state": "open", "events": []}),
        ]

        self.sample_bot_list = "github-actions[bot]\ndependabot[bot]\n"

    def run_actual_feature(self, bot_list, issues):
        with patch("builtins.open", mock_open(read_data=bot_list)):
            with patch("data_loader.DataLoader.get_issues", return_value=issues):
                with patch("features.feature2.plt.show"), \
                     patch("features.feature2.plt.bar") as mock_bar, \
                     patch("features.feature2.plt.text") as mock_text, \
                     patch("config.get_parameter", return_value="mock_path"):
                    # Provide fake bars so plt.text is called
                    mock_bar.return_value = [
                        MagicMock(get_height=MagicMock(return_value=5), get_x=MagicMock(return_value=0), get_width=MagicMock(return_value=1))
                    ]
                    Feature2().run()
                    return mock_bar, mock_text

    def test_run_with_bot_events_executes_plotting(self):
        mock_bar, mock_text = self.run_actual_feature(self.sample_bot_list, self.sample_issues)
        self.assertTrue(mock_bar.called)
        self.assertTrue(mock_text.called)

    def test_run_with_no_bot_events_executes_but_no_plot(self):
        issues = [
            Issue({"state": "open", "events": [
                {"author": "user1"},
                {"author": "user2"},
            ]})
        ]
        with patch("features.feature2.plt.show") as mock_show, \
             patch("config.get_parameter", return_value="mock_path"), \
             patch("builtins.open", mock_open(read_data=self.sample_bot_list)), \
             patch("data_loader.DataLoader.get_issues", return_value=issues):
            Feature2().run()
            mock_show.assert_called_once()

    def test_run_with_empty_bot_list_does_not_fail(self):
        with patch("features.feature2.plt.show") as mock_show, \
             patch("config.get_parameter", return_value="mock_path"), \
             patch("builtins.open", mock_open(read_data="")), \
             patch("data_loader.DataLoader.get_issues", return_value=self.sample_issues):
            Feature2().run()
            mock_show.assert_called_once()

    def test_run_with_empty_issues_does_not_fail(self):
        with patch("features.feature2.plt.show") as mock_show, \
             patch("config.get_parameter", return_value="mock_path"), \
             patch("builtins.open", mock_open(read_data=self.sample_bot_list)), \
             patch("data_loader.DataLoader.get_issues", return_value=[]):
            Feature2().run()
            mock_show.assert_called_once()

    def test_missing_bot_file_raises(self):
        with patch("builtins.open", side_effect=FileNotFoundError), \
             patch("config.get_parameter", return_value="mock_path"), \
             patch("data_loader.DataLoader.get_issues", return_value=[]):
            feature = Feature2()
            with self.assertRaises(FileNotFoundError):
                feature.run()

    def test_case_sensitivity_excludes_uppercase_bots(self):
        issues = [
            Issue({"state": "open", "events": [
                {"author": "GITHUB-ACTIONS[BOT]"},
                {"author": "github-actions[bot]"},
            ]})
        ]
        with patch("builtins.open", mock_open(read_data=self.sample_bot_list)), \
             patch("data_loader.DataLoader.get_issues", return_value=issues), \
             patch("features.feature2.plt.show"), \
             patch("features.feature2.plt.bar") as mock_bar, \
             patch("config.get_parameter", return_value="mock_path"):
            mock_bar.return_value = []  # not testing text here
            Feature2().run()
            args, kwargs = mock_bar.call_args
            bots = args[0].tolist() if hasattr(args[0], 'tolist') else []
            self.assertIn("github-actions[bot]", bots)
            self.assertNotIn("GITHUB-ACTIONS[BOT]", bots)

    def test_duplicate_bot_usernames_still_counts_correctly(self):
        issues = [
            Issue({"state": "open", "events": [
                {"author": "github-actions[bot]"},
                {"author": "github-actions[bot]"},
            ]})
        ]
        bot_list = "github-actions[bot]\ngithub-actions[bot]\n"
        with patch("builtins.open", mock_open(read_data=bot_list)), \
             patch("data_loader.DataLoader.get_issues", return_value=issues), \
             patch("features.feature2.plt.show"), \
             patch("features.feature2.plt.bar") as mock_bar, \
             patch("config.get_parameter", return_value="mock_path"):
            mock_bar.return_value = []  # not testing text here
            Feature2().run()
            args, kwargs = mock_bar.call_args
            bots = args[0].tolist() if hasattr(args[0], 'tolist') else []
            self.assertIn("github-actions[bot]", bots)

if __name__ == '__main__':
    unittest.main()