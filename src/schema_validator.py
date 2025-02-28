from typing import Any, Type, Literal

from pydantic import BaseModel
from pydantic import BaseModel, ValidationError, create_model
from pydantic.fields import FieldInfo

from .type_mapping_factory import TypeMappingFactory
from .default import default_manager
from .exceptions import ConfigurationError


class SchemaValidator:
    """Упрощенный валидатор структур данных с использованием динамических моделей Pydantic"""
    
    def __init__(self, factory: TypeMappingFactory = default_manager.factory):
        self.factory = factory
        

    def validate(self, data: dict, schema: dict) -> dict:
        """
        Валидация данных через динамически генерируемые Pydantic-модели.
        
        Аргументы:
            data: Данные для валидации
            schema: Схема в формате {поле: конфигурация типа}
            
        Возвращает:
            dict: Результат валидации в заданном формате
        """
        result = {
            "valid": True,
            "errors": [],
            "stats": {
                "checked_fields": len(schema),
                "failed_fields": 0
            }
        }

        try:
            model = self._build_model(schema)
            model(**data)

        except ValidationError as exc:
            self._parse_errors(exc, result)
            result["valid"] = False
            result["stats"]["failed_fields"] = len(result["errors"])

        return result


    def _build_model(self, schema: dict) -> Type[BaseModel]:
        """Рекурсивное построение Pydantic-модели из схемы"""
        fields = {}
        for name, config in schema.items():
            field_type = self._get_field_type(config)
            fields[name] = (field_type, FieldInfo(...))

        return create_model('DynamicModel', **fields)


    def _get_field_type(self, config: dict) -> Any:
        """Определение типа поля с учетом вложенных структур"""
        if config.get('type') == 'category':
            return self._handle_category_type(config)
        
        if config.get('type') == 'nested':
            return self._build_model(config.get('schema', {}))
        
        return self.factory.map_type(
            config['type'], 
            **config.get('constraints', {})
        )
    

    def _handle_category_type(self, config: dict) -> type:
        allowed = config.get('allowed_values', [])
        if not allowed:
            raise ConfigurationError("Category type requires allowed_values")
        
        return Literal[tuple(allowed)]


    def _parse_errors(self, exc: ValidationError, result: dict) -> None:
        """Парсинг ошибок валидации в унифицированный формат"""
        for error in exc.errors():
            error_path = ".".join(map(str, error["loc"]))
            error_type = error["type"]
            
            result["errors"].append(
                {
                    "path": error_path,
                    "error": error["msg"],
                    "type": error_type,
                    "context": {
                        "input": error.get("input"),
                        "expected_type": self._get_expected_type(error),
                        **error.get("ctx", {})
                    }
                }
            )


    def _get_expected_type(self, error: dict) -> str:
        """Извлечение ожидаемого типа из контекста ошибки"""
        ctx = error.get("ctx", {})

        return ctx.get("expected", str(ctx.get("type_", "unknown")))
