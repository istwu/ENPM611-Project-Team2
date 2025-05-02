import unittest
from unittest.mock import patch, MagicMock
import matplotlib

# Use Agg so no GUI is required
matplotlib.use('Agg')

from features.feature1 import Feature1

class TestFeature1(unittest.TestCase):

    @patch('features.feature1.plt.show')
    @patch('features.feature1.pd.DataFrame')
    @patch('features.feature1.DataLoader')
    def test_run_aggregates_comments_by_label_and_plots(
        self,
        mock_data_loader,   # patch of DataLoader inside feature1
        mock_df_class,       # patch of pd.DataFrame inside feature1
        mock_show           # patch of plt.show inside feature1
    ):
        # --- Arrange ----------------------------------------------------------------
        # Create two fake issues with different labels & event counts
        issue1 = MagicMock()
        issue1.labels = ['bug', 'feature']
        issue1.events = [MagicMock()] * 2   # 2 events

        issue2 = MagicMock()
        issue2.labels = ['bug']
        issue2.events = [MagicMock()] * 4   # 4 events

        # DataLoader().get_issues() returns our two issues
        mock_data_loader.return_value.get_issues.return_value = [issue1, issue2]

        # Make DataFrame(...) return a fake df instance
        fake_df = MagicMock()
        mock_df_class.return_value = fake_df

        # Stub out the groupby chain so we can verify calls:
        group = fake_df.groupby.return_value
        series_after_mean = group.__getitem__.return_value.mean.return_value
        series_after_mean.nlargest.return_value.plot = MagicMock()

        # --- Act --------------------------------------------------------------------
        Feature1().run()

        # --- Assert -----------------------------------------------------------------
        expected_dict = {
            'Labels': ['bug', 'feature', 'bug'],
            'Comments': [2, 2, 4]
        }
        mock_df_class.assert_called_once_with(expected_dict)
        fake_df.groupby.assert_called_once_with('Labels')
        group.__getitem__.assert_called_once_with('Comments')
        group.__getitem__.return_value.mean.assert_called_once()
        series_after_mean.nlargest.assert_called()
        series_after_mean.nlargest.return_value.plot.assert_called_once()
        mock_show.assert_called_once()

    @patch('features.feature1.plt.show')
    @patch('features.feature1.pd.DataFrame')
    @patch('features.feature1.DataLoader')
    def test_run_aggregates_comments_by_label_and_plots_when_issues_with_no_labels(
        self,
        mock_data_loader,   # patch of DataLoader inside feature1
        mock_df_class,       # patch of pd.DataFrame inside feature1
        mock_show           # patch of plt.show inside feature1
    ):
        # --- Arrange ----------------------------------------------------------------
        # Create two fake issues with different labels & event counts
        issue1 = MagicMock()
        issue1.labels = []
        issue1.events = [MagicMock()] * 2   # 2 events

        issue2 = MagicMock()
        issue2.labels = []
        issue2.events = [MagicMock()] * 4   # 4 events

        # DataLoader().get_issues() returns our two issues
        mock_data_loader.return_value.get_issues.return_value = [issue1, issue2]

        # Make DataFrame(...) return a fake df instance
        fake_df = MagicMock()
        mock_df_class.return_value = fake_df

        # Stub out the groupby chain so we can verify calls:
        group = fake_df.groupby.return_value
        series_after_mean = group.__getitem__.return_value.mean.return_value
        series_after_mean.nlargest.return_value.plot = MagicMock()

        # --- Act --------------------------------------------------------------------
        Feature1().run()

        # --- Assert -----------------------------------------------------------------
        expected_dict = {
            'Labels': [],
            'Comments': []
        }
        mock_df_class.assert_called_once_with(expected_dict)
        fake_df.groupby.assert_called_once_with('Labels')
        group.__getitem__.assert_called_once_with('Comments')
        group.__getitem__.return_value.mean.assert_called_once()
        series_after_mean.nlargest.assert_called()
        series_after_mean.nlargest.return_value.plot.assert_called_once()
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()