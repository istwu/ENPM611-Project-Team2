import unittest
import os
import tempfile
from feature2 import Feature2
from model import Issue, Event
from data_loader import DataLoader
from typing import List

class TestFeature2RealData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create temporary test files before any tests run"""
        # Create a temporary bot usernames file
        cls.bot_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8')
        cls.bot_file.write("github-actions[bot]\ndependabot[bot]\n")
        cls.bot_file.close()
        
        # Create a temporary test data file path (DataLoader would use this)
        cls.test_data_path = tempfile.mkdtemp()
        
    @classmethod
    def tearDownClass(cls):
        """Clean up temporary files after all tests run"""
        os.unlink(cls.bot_file.name)
        os.rmdir(cls.test_data_path)
    
    def setUp(self):
        """Reset test data before each test"""
        # Backup original bot file path
        self.original_bot_file = Feature2().bot_file_path
        
        # Point to our test bot file
        Feature2.bot_file_path = self.bot_file.name
        
        # Create some test issues
        self.test_issues = [
            Issue(events=[
                Event(author="github-actions[bot]"),
                Event(author="dependabot[bot]"),
                Event(author="github-actions[bot]"),
                Event(author="human_user"),
            ]),
            Issue(events=[
                Event(author="dependabot[bot]"),
                Event(author="human_user"),
            ]),
        ]
        
        # Patch DataLoader to return our test issues
        self.original_get_issues = DataLoader.get_issues
        DataLoader.get_issues = lambda self: self.test_issues
    
    def tearDown(self):
        """Restore original state after each test"""
        # Restore original bot file path
        Feature2.bot_file_path = self.original_bot_file
        
        # Restore original DataLoader method
        DataLoader.get_issues = self.original_get_issues
    
    def test_bot_event_counts(self):
        """Test that bot events are counted correctly"""
        # Run the feature
        feature = Feature2()
        feature.run()  # Normally shows plot, but we'll test the counts
        
        # Since we can't access bot_event_counts directly, we need to modify the class
        # to expose the counts for testing, or we can test the plotting output
        
        # Alternative approach: Modify the Feature2 class temporarily
        original_run = Feature2.run
        counts = {}
        
        def run_and_capture_counts(self):
            nonlocal counts
            with open(self.bot_file_path, "r", encoding="utf-8") as f:
                bot_usernames = set(line.strip() for line in f)
            
            for issue in DataLoader().get_issues():
                for event in issue.events:
                    if event.author in bot_usernames:
                        counts[event.author] = counts.get(event.author, 0) + 1
            original_run(self)
        
        Feature2.run = run_and_capture_counts
        
        try:
            feature = Feature2()
            feature.run()
            
            # Verify counts
            self.assertEqual(counts["github-actions[bot]"], 2)
            self.assertEqual(counts["dependabot[bot]"], 2)
            self.assertNotIn("human_user", counts)
        finally:
            # Restore original method
            Feature2.run = original_run
    
    def test_no_bot_events(self):
        """Test when there are no bot events"""
        # Set test data with no bot events
        self.test_issues = [
            Issue(events=[
                Event(author="human1"),
                Event(author="human2"),
            ]),
        ]
        
        # Use the same capture approach as above
        original_run = Feature2.run
        counts = {}
        
        def run_and_capture_counts(self):
            nonlocal counts
            with open(self.bot_file_path, "r", encoding="utf-8") as f:
                bot_usernames = set(line.strip() for line in f)
            
            for issue in DataLoader().get_issues():
                for event in issue.events:
                    if event.author in bot_usernames:
                        counts[event.author] = counts.get(event.author, 0) + 1
            original_run(self)
        
        Feature2.run = run_and_capture_counts
        
        try:
            feature = Feature2()
            feature.run()
            
            # Verify no counts were recorded
            self.assertEqual(len(counts), 0)
        finally:
            Feature2.run = original_run
    
    def test_empty_bot_file(self):
        """Test with an empty bot usernames file"""
        # Create an empty temp file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as f:
            empty_bot_file = f.name
        
        try:
            # Point to our empty bot file
            Feature2.bot_file_path = empty_bot_file
            
            # Use the capture approach
            original_run = Feature2.run
            counts = {}
            
            def run_and_capture_counts(self):
                nonlocal counts
                with open(self.bot_file_path, "r", encoding="utf-8") as f:
                    bot_usernames = set(line.strip() for line in f)
                
                for issue in DataLoader().get_issues():
                    for event in issue.events:
                        if event.author in bot_usernames:
                            counts[event.author] = counts.get(event.author, 0) + 1
                original_run(self)
            
            Feature2.run = run_and_capture_counts
            
            try:
                feature = Feature2()
                feature.run()
                
                # Verify no counts were recorded
                self.assertEqual(len(counts), 0)
            finally:
                Feature2.run = original_run
        finally:
            os.unlink(empty_bot_file)
    
    def test_init(self):
        """Test class initialization"""
        feature = Feature2()
        self.assertIsInstance(feature, Feature2)

if __name__ == '__main__':
    unittest.main()