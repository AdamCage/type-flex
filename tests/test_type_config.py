import pytest

from .src import TypeConfig, map_types


def test_custom_type_registration():
    TypeConfig.register_custom_type('coordinates', tuple[float, float])
    assert map_types('coordinates') == tuple[float, float]


def test_config_loading(tmp_path):
    config_content = """
    types:
      currency:
        base_type: decimal
        max_digits: 12
        decimal_places: 4
    """
    
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(config_content)
    
    TypeConfig.load_config(str(config_file))
    decimal_type = map_types('currency')
    assert decimal_type.__fields__['max_digits'].default == 12
    assert decimal_type.__fields__['decimal_places'].default == 4


def test_reserved_type_registration():
    with pytest.raises(ValueError):
        TypeConfig.register_custom_type('int', tuple)  # Reserved type