"""Tests for the Griffe extension."""

from griffe.docstrings.dataclasses import DocstringSectionKind
from griffe.extensions import Extensions
from griffe.loader import GriffeLoader

from griffe_typingdoc import TypingDocExtension


def test_extension() -> None:
    """Load our own package using the extension, assert a parameters section is added to the parsed docstring."""
    loader = GriffeLoader(extensions=Extensions(TypingDocExtension()))
    typingdoc = loader.load_module("griffe_typingdoc")
    sections = typingdoc["TypingDocExtension.on_function_instance"].docstring.parsed
    assert len(sections) == 2
    assert sections[1].kind is DocstringSectionKind.parameters
    assert sections[1].value[1].description == "The Griffe function just instantiated."
