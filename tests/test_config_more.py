import unittest
import os
import config

class TestConfigInternal(unittest.TestCase):
    def setUp(self):
        # reset in-memory config and clear any env
        try:
            del config._config
        except Exception:
            pass
        for v in ['feature','user','label','ENPM611_PROJECT_DATA_PATH','TESTPARAM','NOPE']:
            os.environ.pop(v, None)

    def test_get_default_path_finds_file(self):
        path = config._get_default_path()
        self.assertTrue(path.endswith('config.json'))

    def test_init_config_loads_file(self):
        config._config = None
        config._init_config()
        self.assertIsInstance(config._config, dict)
        self.assertIn('ENPM611_PROJECT_DATA_PATH', config._config)

    def test_set_and_get_parameter_typed(self):
        # JSON-prefix encoding and decoding
        config._config = None
        config.set_parameter('TESTPARAM', {'x': 42})
        self.assertEqual(config.get_parameter('TESTPARAM'), {'x': 42})

    def test_overwrite_from_args_creates_env(self):
        class Args: pass
        args = Args()
        args.foo = 'bar'
        config._config = None
        config.overwrite_from_args(args)
        self.assertEqual(config.get_parameter('foo'), 'bar')

    # def test_get_parameter_default_behavior(self):
    #     # missing and default provided
    #     self.assertEqual(config.get_parameter('NOPE', default=123), 123)
    #     # missing and no default
    #     self.assertIsNone(config.get_parameter('NOPE'))

    def test_convert_to_typed_value(self):
        self.assertEqual(config.convert_to_typed_value(None), None)
        self.assertEqual(config.convert_to_typed_value('{"a":1}'), {'a':1})
        self.assertEqual(config.convert_to_typed_value('not json'), 'not json')
        self.assertEqual(config.convert_to_typed_value(999), 999)

if __name__ == '__main__':
    unittest.main()
