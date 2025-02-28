from typing import Any, Type

from .type_mapping_factory import (
    TypeMap,
    XMLAdapter,
    YAMLAdapter,
    PluginRegistry
)

from .default import default_manager


class TypeConfig:
    """Менеджер конфигурации типов"""
    

    @staticmethod
    def register_custom_type(name: str, handler: Type) -> None:
        """
        Глобальная регистрация кастомного типа
        
        Пример:
        TypeConfig.register_custom_type('geo_point', tuple[float, float])
        """
        if TypeMap.is_reserved(name):
            raise ValueError(f"Type name {name} is reserved")
        
        default_manager.config.register_custom_type(name, handler)


    @staticmethod
    def register_adapter(format: str, adapter: Type):
        """Регистрация нового формата конфигурации"""
        PluginRegistry.register_adapter(format, adapter)

    
    @staticmethod
    def set_decimal_precision(max_digits: int, decimal_places: int) -> None:
        """Глобальная установка точности для decimal"""
        default_manager.factory.set_decimal_precision(max_digits, decimal_places)

    
    @staticmethod
    def load_config(file_path: str) -> None:
        """
        Загрузка конфигурации из файла
        
        Поддерживаемые форматы:
        - YAML (.yaml, .yml)
        - XML (.xml)
        """
        if file_path.endswith(('.yaml', '.yml')):
            config = YAMLAdapter.parse(open(file_path).read())

        elif file_path.endswith('.xml'):
            config = XMLAdapter.to_dict(open(file_path).read())

        else:
            raise ValueError("Unsupported config format")
        
        TypeConfig._update_attributes(default_manager.config, config.get('types', {}))
        TypeConfig._update_attributes(default_manager.factory, config.get('factory', {}))


    @staticmethod
    def _update_attributes(obj: Any, config_dict: dict[str, Any]) -> None:
        for key, value in config_dict.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
