import unittest
from features.feature1 import Feature1

class TestFeature1(unittest.TestCase):
    def test_run_feature(self):  # <-- ✅ must start with 'test_'
        try:
            Feature1().run()
            success = True
        except Exception as e:
            success = False
        self.assertTrue(success)

if __name__ == '__main__':
    unittest.main()

