"""
XML Parser Service
"""

from typing import Any

from lxml import etree

from app.core.exceptions import XMLParsingError
from app.core.parser_base import ParserBase
from app.services.base import BaseService


class XMLParser(BaseService, ParserBase[etree._Element]):
    """
    XML parsing service with security features
    """

    def __init__(self, disable_xxe: bool = True) -> None:
        """
        Initialize XML parser

        Args:
            disable_xxe: Disable XML External Entity processing for security
        """
        BaseService.__init__(self)
        ParserBase.__init__(self)
        self.disable_xxe = disable_xxe
        self._setup_parser()

    def _setup_parser(self) -> None:
        """Setup XML parser with security settings"""
        # Create parser with security settings
        self.parser = etree.XMLParser(
            resolve_entities=not self.disable_xxe,
            no_network=True,
            remove_blank_text=True,
            remove_comments=False,
            remove_pis=False,
            strip_cdata=False,
            recover=False,
        )
        self.logger.info(f"XML parser configured (XXE disabled: {self.disable_xxe})")

    def parse(self, content: str) -> etree._Element:
        """
        Parse XML content

        Args:
            content: XML string to parse

        Returns:
            Parsed XML element tree

        Raises:
            XMLParsingError: If parsing fails
        """
        try:
            # Parse XML string
            root = etree.fromstring(content.encode("utf-8"), parser=self.parser)
            self.logger.info("Successfully parsed XML")
            return root
        except etree.XMLSyntaxError as e:
            self.logger.error(f"XML syntax error: {e}")
            raise XMLParsingError(
                f"Invalid XML syntax: {e}",
                details={
                    "line": e.lineno,
                    "column": e.offset,
                    "error": str(e),
                },
            )
        except Exception as e:
            self.logger.error(f"XML parsing failed: {e}")
            raise XMLParsingError(
                f"Failed to parse XML: {e}",
                details={"error": str(e)},
            )

    def parse_file(self, file_path: str) -> etree._Element:
        """
        Parse XML from file

        Args:
            file_path: Path to XML file

        Returns:
            Parsed XML element tree

        Raises:
            XMLParsingError: If parsing fails
        """
        try:
            tree = etree.parse(file_path, parser=self.parser)
            root = tree.getroot()
            self.logger.info(f"Successfully parsed XML file: {file_path}")
            return root
        except etree.XMLSyntaxError as e:
            self.logger.error(f"XML syntax error in file: {e}")
            raise XMLParsingError(
                f"Invalid XML syntax in file: {e}",
                details={
                    "file": file_path,
                    "line": e.lineno,
                    "column": e.offset,
                    "error": str(e),
                },
            )
        except Exception as e:
            self.logger.error(f"Failed to parse XML file: {e}")
            raise XMLParsingError(
                f"Failed to parse XML file: {e}",
                details={"file": file_path, "error": str(e)},
            )

    def validate(self, content: str) -> bool:
        """
        Validate XML content without full parsing

        Args:
            content: XML string to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            etree.fromstring(content.encode("utf-8"), parser=self.parser)
            return True
        except Exception:
            return False

    def format(self, content: str, **kwargs: Any) -> str:
        """
        Format/beautify XML content

        Args:
            content: XML string to format
            **kwargs: Formatting options (indent, encoding)

        Returns:
            Formatted XML string

        Raises:
            XMLParsingError: If formatting fails
        """
        indent = kwargs.get("indent", 2)
        encoding = kwargs.get("encoding", "utf-8")
        xml_declaration = kwargs.get("xml_declaration", True)

        try:
            root = self.parse(content)
            # Pretty print with indentation
            formatted = etree.tostring(
                root,
                pretty_print=True,
                encoding=encoding,
                xml_declaration=xml_declaration,
            ).decode(encoding)

            self.logger.info("Successfully formatted XML")
            return formatted
        except Exception as e:
            self.logger.error(f"XML formatting failed: {e}")
            raise XMLParsingError(
                f"Failed to format XML: {e}",
                details={"error": str(e)},
            )

    def to_string(
        self,
        element: etree._Element,
        pretty_print: bool = True,
        encoding: str = "utf-8",
    ) -> str:
        """
        Convert XML element to string

        Args:
            element: XML element
            pretty_print: Whether to pretty print
            encoding: Output encoding

        Returns:
            XML string
        """
        return etree.tostring(
            element, pretty_print=pretty_print, encoding=encoding
        ).decode(encoding)

    def get_root_tag(self, content: str) -> str:
        """
        Get root tag name from XML

        Args:
            content: XML string

        Returns:
            Root tag name
        """
        root = self.parse(content)
        return root.tag

    def get_namespaces(self, content: str) -> dict[str, str]:
        """
        Extract namespaces from XML

        Args:
            content: XML string

        Returns:
            Dictionary of namespace prefixes and URIs
        """
        root = self.parse(content)
        return dict(root.nsmap) if root.nsmap else {}

    def count_elements(self, content: str) -> int:
        """
        Count total number of elements in XML

        Args:
            content: XML string

        Returns:
            Number of elements
        """
        root = self.parse(content)
        return len(list(root.iter()))

    def get_depth(self, content: str) -> int:
        """
        Get maximum depth of XML tree

        Args:
            content: XML string

        Returns:
            Maximum depth
        """

        def _get_depth(element: etree._Element, current_depth: int = 0) -> int:
            if len(element) == 0:
                return current_depth
            return max(_get_depth(child, current_depth + 1) for child in element)

        root = self.parse(content)
        return _get_depth(root)

# Made with Bob
