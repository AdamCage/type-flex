import datetime
import uuid
from decimal import Decimal
from enum import Enum
from typing import Type, Any

from pydantic import BaseModel

from .type_map import TypeMap
from .adapters import *


class TypeConfigSchema(BaseModel):
    types: dict[str, dict]
    adapters: dict[str, dict] = {}
    security: dict[str, Any] = {}


class TypeMapperConfig:
    """Конфигурация с поддержкой расширенной системы типов"""
    
    def __init__(self):
        self._type_map = self._default_type_map()
        self._custom_types: dict[str, Type] = {}
        self._special_handlers = self._init_special_handlers()


    @staticmethod
    def _default_type_map() -> dict[TypeMap, Type]:
        """Базовые маппинги для общесистемных типов"""
        return {
            # Примитивы
            TypeMap.INTEGER: int,
            TypeMap.FLOAT: float,
            TypeMap.STRING: str,
            TypeMap.BOOLEAN: bool,
            
            # Временные типы
            TypeMap.DATETIME: datetime.datetime,
            TypeMap.DATE: datetime.date,
            TypeMap.TIME: datetime.time,
            TypeMap.TIMEDELTA: datetime.timedelta,
            
            # Специальные форматы
            TypeMap.UUID: uuid.UUID,
            TypeMap.DECIMAL: Decimal,
            TypeMap.CURRENCY: Decimal,
            
            # Сетевые типы
            TypeMap.IP_ADDRESS: str,
            TypeMap.URL: str,
            TypeMap.EMAIL: str,
            
            # Бинарные данные
            TypeMap.BYTES: bytes,
            TypeMap.BLOB: bytes,
            
            # Комплексные структуры
            TypeMap.JSON: dict,
            TypeMap.XML: str,
            TypeMap.YAML: dict,
            
            # Коллекции
            TypeMap.ARRAY: list,
            TypeMap.TUPLE: tuple,
            TypeMap.SET: set,
            
            # Специфичные
            TypeMap.ENUM: Enum,
            TypeMap.CUSTOM_OBJECT: object
        }


    def _init_adapters(self) -> dict:
        return {
            TypeMap.XML: XMLAdapter,
            TypeMap.YAML: YAMLAdapter,
        }


    def get_adapter(self, dtype: TypeMap):
        return self._adapters.get(dtype)


    def register_custom_type(self, dtype: str, handler: Type) -> None:
        """Регистрация кастомного типа с валидацией имени"""
        if TypeMap.is_reserved(dtype):
            raise ValueError(f"Type name '{dtype}' is reserved")
        
        self._custom_types[dtype] = handler


    def get_type(self, dtype: str) -> Type:
        """Получение типа с приоритетом кастомных обработчиков"""
        if dtype in self._custom_types:
            return self._custom_types[dtype]
        
        try:
            type_key = TypeMap(dtype)
            return self._type_map.get(type_key) or self._special_handlers.get(type_key)
        
        except ValueError:
            raise TypeError(f"Unsupported enterprise type: {dtype}") from None


    def update(self, config_data: dict) -> None:
        validated = TypeConfigSchema(**config_data)
        self._apply_validated_config(validated)
