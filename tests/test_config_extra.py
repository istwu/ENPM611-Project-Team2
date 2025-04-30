import unittest
import os
import json
import config

class TestConvertTypedValue(unittest.TestCase):
    def test_convert_int(self):
        # JSON numbers should parse to int
        self.assertEqual(config.convert_to_typed_value("123"), 123)

    def test_convert_list(self):
        # JSON arrays should parse to Python lists
        self.assertEqual(config.convert_to_typed_value("[1, 2, 3]"), [1, 2, 3])

    def test_convert_invalid_json(self):
        # Non-JSON strings should be returned as-is
        self.assertEqual(config.convert_to_typed_value("not json"), "not json")

    def test_convert_none(self):
        # None should stay None
        self.assertIsNone(config.convert_to_typed_value(None))


class TestGetParameterPrecedence(unittest.TestCase):
    def setUp(self):
        # Clear environment and in-memory cache
        os.environ.pop("STR_PARAM", None)
        os.environ.pop("LIST_PARAM", None)
        config._config = None

    def test_env_string_overrides_file(self):
        os.environ["STR_PARAM"] = "hello"
        # Even though “STR_PARAM” isn’t in config.json, env wins
        self.assertEqual(config.get_parameter("STR_PARAM", default="x"), "hello")

    def test_env_json_prefix(self):
        os.environ["LIST_PARAM"] = "json:[4,5,6]"
        self.assertEqual(config.get_parameter("LIST_PARAM"), [4, 5, 6])

    def test_default_if_missing(self):
        os.environ.pop("MISSING_PARAM", None)
        # Neither env nor file has this, so default used
        self.assertEqual(config.get_parameter("MISSING_PARAM", default="Z"), "Z")


class TestFileConfiguration(unittest.TestCase):
    def setUp(self):
        # Reset config cache so file is reloaded
        config._config = None

    def test_file_loaded_parameter(self):
        # config.json contains ENPM611_PROJECT_DATA_PATH: "poetry.json"
        self.assertEqual(
            config.get_parameter("ENPM611_PROJECT_DATA_PATH"),
            "poetry.json"
        )

if __name__ == "__main__":
    unittest.main()
