import pytest

from .src.type_config import XMLAdapter, YAMLAdapter
from .src.exceptions import SecurityError


def test_yaml_parsing():
    yaml_content = """
    types:
      currency:
        base_type: decimal
        precision: 4
    """
    
    parsed = YAMLAdapter.parse(yaml_content)
    assert 'types' in parsed
    assert parsed['types']['currency']['precision'] == 4


def test_xml_security():
    bomb = '<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol"><!ELEMENT lolz (#PCDATA)>]>'
    
    with pytest.raises(SecurityError):
        XMLAdapter.to_dict(bomb, max_size=100)
