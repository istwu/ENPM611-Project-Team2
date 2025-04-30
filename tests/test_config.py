import unittest
import os
import config

class DummyArgs:
    def __init__(self):
        self.feature = 1
        self.user = 'alice'
        self.label = 'bug'

class TestConfig(unittest.TestCase):
    def setUp(self):
        # Clear environment and in-memory config
        for var in ['feature', 'user', 'label', 'ENPM611_PROJECT_DATA_PATH', 'TESTPARAM', 'NONEXISTENT_PARAM']:
            os.environ.pop(var, None)
        try:
            # Reset the internal cache
            config._config = None
        except AttributeError:
            pass

    def test_default_data_path_from_file(self):
        # config.json specifies the data path
        val = config.get_parameter('ENPM611_PROJECT_DATA_PATH')
        self.assertEqual(val, 'poetry.json')

    def test_overwrite_from_args_sets_env(self):
        args = DummyArgs()
        config.overwrite_from_args(args)
        # get_parameter reads env first
        self.assertEqual(config.get_parameter('feature'), 1)
        self.assertEqual(config.get_parameter('user'), 'alice')
        self.assertEqual(config.get_parameter('label'), 'bug')

    def test_set_and_get_parameter_typed(self):
        # non-string values are stored as JSON-prefixed
        config.set_parameter('TESTPARAM', {'x': 2})
        got = config.get_parameter('TESTPARAM')
        self.assertEqual(got, {'x': 2})

    def test_empty_config_when_no_file(self):
        """
        Simulate no config.json on disk: _init_config should set _config to {},
        and get_parameter should return the provided default.
        """
        cwd = os.getcwd()
        # Move into a directory without config.json (the tests/ folder)
        os.chdir(os.path.join(cwd, 'tests'))
        try:
            config._config = None
        except AttributeError:
            pass

        # Ask for a non-existent parameter with a default
        val = config.get_parameter('NONEXISTENT_PARAM', default='Z')
        self.assertEqual(val, 'Z')

        # Restore working directory
        os.chdir(cwd)

if __name__ == '__main__':
    unittest.main()
