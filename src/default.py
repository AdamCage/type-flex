from .type_mapping_factory import TypeMappingFactory, TypeMapperConfig


class ConfigManager:
    _instance = None
    
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.reset()

        return cls._instance
    

    def reset(self):
        self.config = TypeMapperConfig()
        self.factory = TypeMappingFactory(self.config)


default_manager = ConfigManager()
