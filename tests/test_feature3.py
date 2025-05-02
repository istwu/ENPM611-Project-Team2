import unittest
from unittest.mock import patch
from features.feature3 import Feature3
from model import Issue

class TestFeature3(unittest.TestCase):

    '''
    Tests that issue/event counts for each user are calculated accurately
    ''' 
    @patch('features.feature3.DataLoader')
    def test_count_issues_and_events_by_user(self, mock_data_loader):
        # Setup mock data
        mock_issues = [
            Issue({
                'creator': 'alice',
                'state': 'open',
                'events': [
                    {'author':'alice'},
                    {'author':'bob'}
                ]
            }),
            Issue({
                'creator': 'bob',
                'state': 'open',
                'events': [
                    {'author':'alice'},
                    {'author':'alice'}
                ]
            }),
            Issue({
                'creator': 'alice',
                'state': 'open',
                'events': []
            })
        ]

        mock_data_loader.return_value.get_issues.return_value = mock_issues

        with patch('builtins.print') as mock_print:
            feature = Feature3()
            feature.count_issues_and_events_by_user('alice')
            mock_print.assert_called_with('alice has created 2 issues and 3 issue comments/events.')

    '''
    Tests that users who have not contributed issues/events are 
    not counted
    '''
    @patch('features.feature3.DataLoader')
    def test_count_issues_and_events_by_user_no_matches(self, mock_data_loader):
        mock_issues = [
            Issue({
                'creator': 'charlie',
                'state': 'closed',
                'events': [
                    {'author': 'charlie'}
                ]
            })
        ]
        mock_data_loader.return_value.get_issues.return_value = mock_issues

        with patch('builtins.print') as mock_print:
            feature = Feature3()
            feature.count_issues_and_events_by_user('alice')
            mock_print.assert_called_with('alice has created 0 issues and 0 issue comments/events.')

    '''
    Tests for equivalent usernames with different capitalization 
    '''
    @patch('features.feature3.DataLoader')
    def test_case_sensitive_username(self, mock_data_loader):
        mock_issues = [
            Issue({
                'creator': 'alice',
                'state': 'open',
                'events': [
                    {'author': 'alice'}
                ]
            })
        ]
        mock_data_loader.return_value.get_issues.return_value = mock_issues

        with patch('builtins.print') as mock_print:
            feature = Feature3()
            feature.count_issues_and_events_by_user('Alice')
            mock_print.assert_called_with('Alice has created 0 issues and 0 issue comments/events.')

    '''
    Test behavior on empty issues list
    '''
    @patch('features.feature3.DataLoader')
    def test_empty_issues(self, mock_data_loader):
        mock_data_loader.return_value.get_issues.return_value = []

        with patch('builtins.print') as mock_print:
            feature = Feature3()
            feature.count_issues_and_events_by_user('alice')
            mock_print.assert_called_with('alice has created 0 issues and 0 issue comments/events.')

    '''
    Test handling for blank input
    '''
    @patch('features.feature3.DataLoader')
    def test_empty_username(self, mock_data_loader):
        mock_issues = [
            Issue({
                'creator': 'alice',
                'state': 'open',
                'events': [
                    {'author': 'alice'}
                ]
            })
        ]
        mock_data_loader.return_value.get_issues.return_value = mock_issues

        with patch('builtins.print') as mock_print:
            feature = Feature3()
            feature.count_issues_and_events_by_user('')
            mock_print.assert_called_with(' has created 0 issues and 0 issue comments/events.')

if __name__ == '__main__':
    unittest.main()
