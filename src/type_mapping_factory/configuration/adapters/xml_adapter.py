from typing import Any, Optional

import xml.etree.ElementTree as ET
from xml.dom import minidom
from defusedxml.ElementTree import fromstring
from defusedxml.common import DefusedXmlException

from ....exceptions import SecurityError, XMLProcessingError


class XMLAdapter:
    """XML processing adapter with validation and transformation capabilities"""
    
    @classmethod
    def validate(cls, xml_str: str, schema: Optional[Any] = None) -> bool:
        """
        Validate XML structure with optional schema validation
        
        Args:
            xml_str: XML content as string
            schema: Optional schema validator (XSD, DTD etc.)
            
        Returns:
            bool: True if XML is valid, False otherwise
        """
        try:
            # Basic syntax validation
            ET.fromstring(xml_str)
            
            # Schema validation if provided
            if schema:
                return cls._validate_with_schema(xml_str, schema)
                
            return True
        
        except ET.ParseError as e:
            return False
        
        except Exception as e:
            return False
        

    @staticmethod
    def _validate_with_schema(xml_str: str, schema: Any) -> bool:
        """Internal method for schema validation"""
        # Implementation depends on schema type
        # Example for XSD validation would go here
        raise NotImplementedError("Schema validation not implemented")


    @classmethod
    def to_dict(cls, xml_str: str, max_size: int = 10 * 1024 * 1024) -> dict:
        """Безопасный парсинг XML с лимитом размера"""
        if len(xml_str) > max_size:
            raise SecurityError("XML size exceeds allowed limit")
        
        try:
            root = fromstring(xml_str, forbid_dtd=True, forbid_entities=True)
            return cls._element_to_dict(root)
        
        except DefusedXmlException as e:
            raise XMLProcessingError(f"XML parsing failed: {str(e)}")


    @staticmethod
    def _element_to_dict(element: ET.Element) -> dict[str, Any]:
        """Recursive helper for XML to dict conversion"""
        return {
            **element.attrib,
            "text": element.text.strip() if element.text else None,
            "children": {child.tag: XMLAdapter._element_to_dict(child) for child in element}
        }


    @classmethod
    def from_dict(cls, data: dict[str, Any], root_tag: str = "root") -> str:
        """Generate XML from dictionary structure"""
        root = ET.Element(root_tag)
        cls._dict_to_element(data, root)

        return minidom.parseString(ET.tostring(root)).toprettyxml()


    @staticmethod
    def _dict_to_element(data: dict[str, Any], parent: ET.Element):
        """Recursive helper for dict to XML conversion"""
        for key, value in data.items():
            if key == "text":
                parent.text = str(value)

            elif key == "children":
                for child_key, child_value in value.items():
                    element = ET.SubElement(parent, child_key)
                    XMLAdapter._dict_to_element(child_value, element)

            else:
                parent.set(key, str(value))