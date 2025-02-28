"""
Type Flex Framework

Основные сущности:
- TypeMappingFactory: Центральный класс фабрики
- map_types: Глобальная функция маппинга
- SchemaValidator: Валидатор структур данных
- TypeConfig: Конфигурационный менеджер
"""
import logging
from typing import Any
from functools import lru_cache

from .type_mapping_factory import TypeMappingFactory, TypeMapperConfig
from .data_model import DataModel
from .default import default_manager
from .schema_validator import SchemaValidator
from .type_config import TypeConfig


logger = logging.getLogger(__name__)


# Кэширование часто используемых типов
@lru_cache(maxsize=256)
def map_types(dtype: str, **kwargs) -> Any:
    """
    Глобальный интерфейс маппинга типов с кэшированием
    
    Примеры:
    >>> map_types('int')
    <class 'int'>
    
    >>> map_types('decimal', gt=0)
    pydantic.types.ConstrainedDecimal
    
    >>> map_types('ip_address')
    pydantic.types.IPvAnyAddress
    """
    try:
        return default_manager.factory.map_type(dtype, **kwargs)
    
    except Exception as e:
        logger.error(f'Mapping failed for {dtype}: {str(e)}')
        raise e


def reset_global_config() -> None:
    """Сброс глобальной конфигурации к значениям по умолчанию"""
    default_manager.reset()
    default_manager.factory.clear_cache()


__all__ = [
    "TypeConfig",
    "TypeMappingFactory",
    "TypeMapperConfig",
    "DataModel",
    "SchemaValidator",
    "default_manager",
    "reset_global_config"
]
