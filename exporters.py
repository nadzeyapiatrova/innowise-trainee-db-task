import json
import xml.etree.ElementTree as ET


class JsonExporter:
    """A class for saving to JSON."""

    def export(self, data, filepath):
        # Converting complex data types (dates, intervals) into standard strings
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4, default=str)
        print(f"File saved: {filepath}")


class XmlExporter:
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
    """Simple factory: returns the appropriate class based on the format name."""

    @classmethod
    def get_exporter(cls, format_type):
        format_type = format_type.lower()
        if format_type == "json":
            return JsonExporter()
        elif format_type == "xml":
            return XmlExporter()
        else:
            raise ValueError(f"Unknown format: {format_type}")
        