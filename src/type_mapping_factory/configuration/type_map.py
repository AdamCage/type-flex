from enum import Enum


class TypeMap(str, Enum):
    """Data types with extended validation support."""
    # Basic types
    INTEGER = "int"
    FLOAT = "float"
    STRING = "str"
    BOOLEAN = "bool"

    # Categorical types
    CATEGORY = "category"
    
    # Temporal types
    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"
    TIMEDELTA = "timedelta"
    
    # Special formats
    UUID = "uuid"
    DECIMAL = "decimal"
    CURRENCY = "currency"
    
    # Network types
    IP_ADDRESS = "ip_address"
    URL = "url"
    EMAIL = "email"
    
    # Binary data
    BYTES = "bytes"
    BLOB = "blob"
    
    # Complex structures
    JSON = "json"
    XML = "xml"
    YAML = "yaml"
    
    # Collections
    ARRAY = "array"
    TUPLE = "tuple"
    SET = "set"
    
    # Database-specific
    JSONB = "jsonb"
    ENUM = "enum"
    
    # Custom
    CUSTOM_OBJECT = "custom_object"


    @classmethod
    def is_reserved(cls, value: str) -> bool:
        """Проверка на зарезервированное имя типа"""
        return value in cls._value2member_map_
