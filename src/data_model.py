from typing import Type

from pydantic import BaseModel


class DataModel(BaseModel):
    """Базовый класс для моделей данных с автоматическим маппингом"""
    

    @classmethod
    def build_model(cls, schema: dict[str, dict]) -> Type[BaseModel]:
        """
        Динамическое создание модели Pydantic
        
        Аргументы:
            schema: Схема данных в формате {поле: конфигурация}
            
        Пример:
        schema = {
            'email': {'type': 'email'},
            'coordinates': {'type': 'geo_point'}
        }
        UserModel = DataModel.build_model(schema)
        """
        fields = {}
        for name, config in schema.items():
            field_type = map_types(config['type'], **config.get('constraints', {}))
            fields[name] = (field_type, ...)
        
        return type('DynamicModel', (cls,), {'__annotations__': fields})
