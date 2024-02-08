"""Tests for the Griffe extension."""

from griffe.docstrings.dataclasses import DocstringSectionKind
from griffe.extensions import Extensions
from griffe.loader import GriffeLoader
from griffe.tests import temporary_visited_package

from griffe_typingdoc import TypingDocExtension

typing_imports = (
    "from typing import Annotated, Doc, Generator, Iterator, Name, NotRequired, Raises, TypedDict, Unpack, Warns"
)
warning_imports = "from warnings import deprecated"

# NOTE: Important! The value in calls to `Doc` will be parsed as a Name expression
# if it is valid Python syntax for names. To make sure it is correctly parsed as a string,
# it must contain invalid syntax for names, such as a dot at the end.
# The alternative solution would be to add `from __future__ import annotations`
# at the beginning of each temporary visited module.


def test_extension_on_itself() -> None:
    """Load our own package using the extension, assert a parameters section is added to the parsed docstring."""
    loader = GriffeLoader(extensions=Extensions(TypingDocExtension()))
    typingdoc = loader.load("griffe_typingdoc")
    sections = typingdoc["TypingDocExtension.on_function_instance"].docstring.parsed
    assert len(sections) == 2
    assert sections[1].kind is DocstringSectionKind.parameters
    assert sections[1].value[1].description == "The Griffe function just instantiated."


def test_attribute_doc() -> None:
    """Read documentation for attributes."""
    with temporary_visited_package(
        "package",
        modules={"__init__.py": f"{typing_imports}\na: Annotated[str, Doc('Hello.')]"},
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        assert package["a"].docstring.value == "Hello."


def test_parameter_doc() -> None:
    """Read documentation for parameters."""
    with temporary_visited_package(
        "package",
        modules={"__init__.py": f"{typing_imports}\ndef f(a: Annotated[str, Doc('Hello.')]): ..."},
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        assert package["f"].docstring.parsed[1].value[0].description == "Hello."


def test_other_parameter_doc() -> None:
    """Read documentation for other parameters, in unpack/typeddict annotations."""
    with temporary_visited_package(
        "package",
        modules={
            "__init__.py": f"""
                {typing_imports}
                class OtherParameters(TypedDict, total=False):
                    param1: Annotated[NotRequired[str], Doc("Hello.")]

                def f(**kwargs: Annotated[Unpack[OtherParameters], Doc("See other parameters.")]):
                    ...
            """,
        },
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        assert package["f"].docstring.parsed[2].value[0].description == "Hello."


def test_iterator_doc() -> None:
    """Read documentation in iterator annotations."""
    with temporary_visited_package(
        "package",
        modules={
            "__init__.py": f"""
                {typing_imports}
                def f() -> Iterator[Annotated[int, Doc("Yielded hello.")]]:
                    ...
            """,
        },
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        assert package["f"].docstring.parsed[1].value[0].description == "Yielded hello."


def test_generator_doc() -> None:
    """Read documentation in generator annotations."""
    with temporary_visited_package(
        "package",
        modules={
            "__init__.py": f"""
                {typing_imports}
                def f() -> Generator[
                    Annotated[int, Doc("Yielded hello.")],
                    Annotated[int, Doc("Received hello.")],
                    Annotated[int, Doc("Returned hello.")],
                ]:
                    ...
            """,
        },
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        sections = package["f"].docstring.parsed
        assert sections[1].value[0].description == "Yielded hello."
        assert sections[2].value[0].description == "Received hello."
        assert sections[3].value[0].description == "Returned hello."


def test_generator_tuples() -> None:
    """Read documentation in generator annotations (in tuples)."""
    with temporary_visited_package(
        "package",
        modules={
            "__init__.py": f"""
                {typing_imports}
                def f() -> Generator[
                    tuple[
                        Annotated[int, Doc("First yielded.")],
                        Annotated[float, Doc("Second yielded.")],
                    ],
                    tuple[
                        Annotated[int, Doc("First received.")],
                        Annotated[float, Doc("Second received.")],
                    ],
                    tuple[
                        Annotated[int, Doc("First returned.")],
                        Annotated[float, Doc("Second returned.")],
                    ],
                ]:
                    ...
            """,
        },
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        sections = package["f"].docstring.parsed
        assert sections[1].value[0].description == "First yielded."
        assert sections[1].value[1].description == "Second yielded."
        assert sections[2].value[0].description == "First received."
        assert sections[2].value[1].description == "Second received."
        assert sections[3].value[0].description == "First returned."
        assert sections[3].value[1].description == "Second returned."


def test_return_doc() -> None:
    """Read documentation for return value."""
    with temporary_visited_package(
        "package",
        modules={"__init__.py": f"{typing_imports}\ndef f() -> Annotated[int, Doc('Hello.')]: ..."},
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        assert package["f"].docstring.parsed[1].value[0].description == "Hello."
