import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class BaseExporter(ABC):
    """Abstract base class defining the contract for all exporters."""

    @abstractmethod
    def export(self, data, filepath):
        pass

class JsonExporter(BaseExporter):
    """A class for saving to JSON."""

    def export(self, data, filepath):
        # Converting complex data types (dates, intervals) into standard strings
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4, default=str)
        print(f"File saved: {filepath}")


class XmlExporter(BaseExporter):
    """A class for saving to XML."""

    def export(self, data, filepath):
        # Create a root tag <results>
        root = ET.Element("results")

        # Add each line as a separate block <item>
        for row in data:
            item = ET.SubElement(root, "item")
            for key, val in row.items():
                child = ET.SubElement(item, str(key))
                child.text = str(val) if val is not None else ""

        # Save the constructed XML tree to a file
        tree = ET.ElementTree(root)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
        print(f"File saved: {filepath}")


class ExporterFactory:
    """Factory returning the appropriate exporter based on format name."""

    _exporters = {
        "json": JsonExporter,
        "xml": XmlExporter,
    }

    @classmethod
    def get_exporter(cls, format_type):
        exporter_class = cls._exporters.get(format_type.lower())
        if not exporter_class:
            raise ValueError(f"Unknown format: {format_type}")
        return exporter_class()
        