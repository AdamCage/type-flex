class TypeMapperError(Exception):
    """Base exception with context capture"""
    def __init__(self, message: str, context: dict = None):
        super().__init__(message)
        self.context = context or {}


class InvalidTypeMappingError(TypeMapperError):
    """Detailed mapping error with type info"""
    def __init__(self, dtype: str, constraint: str = None):
        super().__init__(f"Invalid mapping for type {dtype}", {'dtype': dtype, 'constraint': constraint})


class MappingError(TypeMapperError):
    """Ошибка маппинга типов"""


class SecurityError(TypeMapperError):
    """Ошибка безопасности данных"""


class ConfigurationError(TypeMapperError):
    """Ошибка конфигурации"""


class XMLProcessingError(TypeMapperError):
    """Ошибка обработки XML"""
