import pytest

from src import reset_global_config
from src.type_config import TypeConfig, XMLAdapter, YAMLAdapter


@pytest.fixture(autouse=True)
def reset_config():
    """Сброс конфигурации перед каждым тестом"""
    reset_global_config()

    TypeConfig.register_adapter('yaml', YAMLAdapter)
    TypeConfig.register_adapter('xml', XMLAdapter)
