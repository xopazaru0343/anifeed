from unittest.mock import patch, mock_open
from anifeed.utils.commons import UniversalPath, DictWrangler, TomlParser


class TestUniversalPath:
    def test_path_creation(self):
        path = UniversalPath("test/path")
        assert "test" in str(path)
        assert "path" in str(path)

    def test_path_division(self):
        path = UniversalPath("base")
        new_path = path / "subdir" / "file.txt"

        assert "base" in str(new_path)
        assert "subdir" in str(new_path)
        assert "file.txt" in str(new_path)

    def test_path_fspath(self):
        import os
        path = UniversalPath("test")
        assert os.fspath(path) == str(path)


class TestDictWrangler:
    def test_find_value_in_flat_dict(self):
        data = {"key1": "value1", "key2": "value2"}
        result = DictWrangler.find_value_recursively(data, "key1")
        assert result == "value1"

    def test_find_value_in_nested_dict(self):
        """Test finding value in nested dictionary"""
        data = {
            "level1": {
                "level2": {
                    "target": "found"
                }
            }
        }
        result = DictWrangler.find_value_recursively(data, "target")
        assert result == "found"

    def test_find_value_in_list(self):
        data = {
            "items": [
                {"id": 1, "name": "first"},
                {"id": 2, "name": "second", "target": "found"}
            ]
        }
        result = DictWrangler.find_value_recursively(data, "target")
        assert result == "found"

    def test_find_value_not_found(self):
        data = {"key1": "value1"}
        result = DictWrangler.find_value_recursively(data, "nonexistent")
        assert result is None


class TestTomlParser:
    @patch("builtins.open", new_callable=mock_open, read_data=b"[section]\nkey = 'value'")
    @patch('anifeed.utils.commons.tomllib.load')
    def test_get_config(self, mock_load, mock_file):
        """Test getting config from TOML"""
        mock_load.return_value = {"section": {"key": "value"}}

        result = TomlParser.get_config("section")

        assert result == {"key": "value"}
        mock_file.assert_called_once()
