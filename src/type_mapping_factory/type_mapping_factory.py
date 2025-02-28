import logging
from functools import lru_cache
from typing import Optional, Type, Literal

from pydantic import (
    condecimal,
    confloat,
    conint,
    AnyUrl,
    EmailStr,
    IPvAnyAddress,
    StrictStr
)
from pydantic.types import condecimal as PydanticConDecimal


from .configuration import TypeMapperConfig, DecimalPrecision
from .configuration import TypeMap
from .configuration import XMLAdapter
from .configuration import YAMLAdapter


logger = logging.getLogger(__name__)


class TypeMappingFactory:
    """Type mapping factory with extended data support"""

    allowed_constraints = {
        'ge',
        'gt',
        'le',
        'lt', 
        'multiple_of',
        'allow_inf_nan'
    }
    
    
    def __init__(self, config: Optional[TypeMapperConfig] = None):
        self.config = config or TypeMapperConfig()
        self._precision_config = DecimalPrecision()
        self._constraint_handlers = self._init_constraint_handlers()
        self._cache = {}


    def _init_constraint_handlers(self) -> dict:
        """Инициализация обработчиков ограничений для специальных типов"""
        return {
            TypeMap.IP_ADDRESS: IPvAnyAddress,
            TypeMap.URL: AnyUrl,
            TypeMap.EMAIL: EmailStr,
            TypeMap.XML: self._handle_xml_type,
            TypeMap.YAML: self._handle_yaml_type,
            TypeMap.CURRENCY: self._handle_currency_type,
            TypeMap.CATEGORY: self._handle_category_type
        }
    

    def set_decimal_precision(self, max_digits: int, decimal_places: int) -> None:
        """Установка точности для decimal и связанных типов"""
        self._precision_config = DecimalPrecision(max_digits, decimal_places)


    def clear_cache(self):
        self._cache.clear()


    def _handle_xml_type(self, **constraints) -> Type:
        """Обработчик XML типа с валидацией"""
        if 'schema' in constraints:
            return XMLAdapter.get_validator(constraints['schema'])
        return XMLAdapter
    

    def _handle_yaml_type(self, **constraints) -> Type:
        """Обработчик YAML типа с поддержкой слияния"""
        if 'merge' in constraints:
            return YAMLAdapter.get_merger(**constraints)
        return YAMLAdapter
    

    def _handle_currency_type(self, **constraints) -> PydanticConDecimal:
        """Обработчик валюты с автоматической привязкой к точности"""
        return condecimal(
            max_digits=self._precision_config.max_digits,
            decimal_places=self._precision_config.decimal_places,
            **constraints
        )


    def _handle_category_type(self, **constraints) -> type:
        """Обработчик категориальных значений"""
        allowed = constraints.get('allowed_values')
        
        if not allowed or not isinstance(allowed, (list, tuple, set)):
            raise ValueError("Category type requires 'allowed_values' constraint")
        
        return Literal[tuple(allowed)] if len(allowed) > 1 else StrictStr


    @lru_cache(maxsize=1024)
    def map_type(self, dtype: str, **constraints) -> Type | PydanticConDecimal:
        """Основной метод маппинга типов с расширенной логикой"""

        if constraints:
            validated_constraints = {k: v for k, v in constraints.items() if k in self.allowed_constraints}

        try:
            base_type = self.config.get_type(dtype)
            type_enum = TypeMap(dtype) if TypeMap.is_reserved(dtype) else None

            if handler := self._constraint_handlers.get(type_enum):
                return handler(**validated_constraints) if callable(handler) else handler

            if constraints:
                if type_enum == TypeMap.INTEGER:
                    return conint(**validated_constraints)
                
                if type_enum == TypeMap.FLOAT:
                    return confloat(**validated_constraints)

            if type_enum in (TypeMap.DECIMAL, TypeMap.CURRENCY):
                return condecimal(
                    max_digits=self._precision_config.max_digits,
                    decimal_places=self._precision_config.decimal_places,
                    **validated_constraints
                )

            return base_type

        except ValueError as e:
            logger.error(f"Unsupported type: {dtype}: {str(e)}")
            raise TypeError(f"Unsupported type: {dtype}") from e
        
        except Exception as e:
            logger.error(f"Type mapping failed for {dtype}: {str(e)}")
            raise RuntimeError(f"Type mapping failed for {dtype}") from e


    def bulk_map_types(self, type_schema: dict) -> dict:
        """Пакетный маппинг типов для схем данных"""
        return {
            k: self.map_type(v['type'], **v.get('constraints', {}))
            for k, v in type_schema.items()
        }


    @classmethod
    def from_config_file(cls, config_path: str) -> 'TypeMappingFactory':
        """Фабричный метод для инициализации из конфигурационного файла"""
        if config_path.endswith('.yaml'):
            config = YAMLAdapter.load_config(config_path)

        elif config_path.endswith('.xml'):
            config = XMLAdapter.parse_config(config_path)

        else:
            raise ValueError("Unsupported config format")
        
        return cls(TypeMapperConfig(**config))
    