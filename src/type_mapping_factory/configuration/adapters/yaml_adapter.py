from typing import Any

import yaml
from yaml import YAMLError


class YAMLAdapter:
    """YAML processing adapter with safe loading and error handling"""
    
    @classmethod
    def validate(cls, yaml_str: str) -> bool:
        """
        Validate YAML syntax
        
        Args:
            yaml_str: YAML content as string
            
        Returns:
            bool: True if valid YAML, False otherwise
        """
        try:
            yaml.safe_load(yaml_str)
            return True
        
        except YAMLError as e:
            return False


    @classmethod
    def parse(cls, yaml_str: str, safe: bool = True) -> dict[str, Any]:
        """
        Parse YAML to Python dict with optional safe mode
        
        Args:
            yaml_str: YAML content as string
            safe: Use safe loader (recommended)
            
        Returns:
            dict: Parsed YAML content
            
        Raises:
            ValueError: On parsing failure
        """
        try:
            loader = yaml.SafeLoader if safe else yaml.Loader
            return yaml.load(yaml_str, Loader=loader)
        
        except YAMLError as e:
            raise ValueError("Invalid YAML format") from e


    @classmethod
    def to_yaml(cls, data: dict[str, Any], **kwargs) -> str:
        """
        Convert Python object to YAML string
        
        Args:
            data: Data structure to serialize
            kwargs: Additional arguments for dumper
            
        Returns:
            str: YAML-formatted string
        """
        try:
            return yaml.dump(
                data,
                Dumper=yaml.SafeDumper,
                default_flow_style=False,
                **kwargs
            )
        
        except yaml.YAMLError as e:
            raise ValueError("YAML conversion failed") from e

    @classmethod
    def merge_yaml(cls, *yaml_strs: str) -> dict[str, Any]:
        """
        Merge multiple YAML documents
        
        Args:
            *yaml_strs: YAML strings to merge
            
        Returns:
            dict: Merged configuration
        """
        result = {}
        for yaml_str in yaml_strs:
            try:
                result.update(yaml.safe_load(yaml_str))

            except (YAMLError, TypeError) as e:
                print(f"Skipping invalid YAML document: {str(e)}")
                
        return result
