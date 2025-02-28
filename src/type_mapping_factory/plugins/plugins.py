from typing import Type


class PluginRegistry:
    _adapters: dict[str, Type] = {}
    _type_handlers: dict[str, Type] = {}


    @classmethod
    def register_adapter(cls, format: str, adapter: Type):
        if not hasattr(adapter, 'parse') or not callable(adapter.parse):
            raise TypeError("Adapter must implement parse() method")
        
        cls._adapters[format.lower()] = adapter


    @classmethod
    def get_adapter(cls, format: str) -> Type:
        return cls._adapters.get(format.lower())