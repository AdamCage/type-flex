from decimal import Decimal

import pytest
from pydantic import EmailStr, IPvAnyAddress

from .src import map_types, TypeMappingFactory


def test_basic_type_mapping():
    assert map_types('int') is int
    assert map_types('str') is str
    assert map_types('bool') is bool


def test_constrained_types():
    decimal_type = map_types('decimal', gt=0, max_digits=10)
    assert issubclass(decimal_type, Decimal)
    assert decimal_type.__fields__['gt'].default == 0


def test_special_types():
    assert map_types('email') is EmailStr
    assert map_types('ip_address') is IPvAnyAddress


def test_cached_mapping():
    map_types('int')
    with pytest.raises(AttributeError):
        map_types.cache_clear()


def test_invalid_type_mapping():
    with pytest.raises(TypeError):
        map_types('invalid_type')


def test_factory_precision_config():
    factory = TypeMappingFactory()
    factory.set_decimal_precision(10, 2)
    decimal_type = factory.map_type('decimal')
    assert decimal_type.__fields__['max_digits'].default == 10
    assert decimal_type.__fields__['decimal_places'].default == 2
