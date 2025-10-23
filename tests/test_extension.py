"""Tests for the Griffe extension."""

import pytest
from griffe import DocstringSectionKind, Extensions, GriffeLoader, temporary_visited_package

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


def test_unpacking_typed_dict() -> None:
    """Unpack typed dicts, resolving them to their right location."""
    with temporary_visited_package(
        "package",
        {
            "__init__.py": """
                from typing import TypedDict
                from typing_extensions import Annotated, Doc, Unpack

                from package import module

                class Options(TypedDict):
                    foo: Annotated[int, Doc("Foo's description.")]

                class A:
                    def __init__(self, **kwargs: Unpack[Options]) -> None:
                        '''Init.'''
                        self.options = kwargs

                class B:
                    def __init__(self, **kwargs: Unpack[module.Options]) -> None:
                        '''Init.'''
                        self.options = kwargs
                """,
            "module.py": """
                from typing import TypedDict
                from typing_extensions import Annotated, Doc

                class Options(TypedDict):
                    bar: Annotated[str, Doc("Bar's description.")]
                """,
        },
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        sections = package["A.__init__"].docstring.parsed
        assert len(sections) == 2
        assert sections[0].kind is DocstringSectionKind.text
        assert sections[1].kind is DocstringSectionKind.other_parameters
        foo = sections[1].value[0]
        assert foo.name == "foo"
        assert foo.description == "Foo's description."
        assert str(foo.annotation).startswith("Annotated[int")

        sections = package["B.__init__"].docstring.parsed
        assert len(sections) == 2
        assert sections[0].kind is DocstringSectionKind.text
        assert sections[1].kind is DocstringSectionKind.other_parameters
        bar = sections[1].value[0]
        assert bar.name == "bar"
        assert bar.description == "Bar's description."
        assert str(bar.annotation).startswith("Annotated[str")


@pytest.mark.parametrize(
    "annotation",
    ["int", "Annotated[int, '']"],
)
def test_ignore_unannotated_params(annotation: str) -> None:
    """Ignore parameters that are not annotated with `Doc`."""
    with temporary_visited_package(
        "package",
        {
            "__init__.py": f"{typing_imports}\ndef f(a: {annotation}):\n    '''Docstring.'''",
        },
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        sections = package["f"].docstring.parsed
        assert len(sections) == 1
        assert sections[0].kind is DocstringSectionKind.text


@pytest.mark.parametrize(
    "annotation",
    ["int", "Annotated[int, '']"],
)
def test_ignore_unannotated_other_params(annotation: str) -> None:
    """Ignore other parameters that are not annotated with `Doc`."""
    with temporary_visited_package(
        "package",
        {
            "__init__.py": f"""
            {typing_imports}
            from typing import TypedDict
            class Kwargs(TypedDict):
                a: {annotation}
            def f(**kwargs: Unpack[Kwargs]):
                '''Docstring.'''
            """,
        },
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        sections = package["f"].docstring.parsed
        assert len(sections) == 1
        assert sections[0].kind is DocstringSectionKind.text


@pytest.mark.parametrize(
    "annotation",
    ["int", "Annotated[int, '']"],
)
def test_ignore_unannotated_returns(annotation: str) -> None:
    """Ignore return values that are not annotated with `Doc`."""
    with temporary_visited_package(
        "package",
        {
            "__init__.py": f"{typing_imports}\ndef f() -> {annotation}:\n    '''Docstring.'''",
        },
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        sections = package["f"].docstring.parsed
        assert len(sections) == 1
        assert sections[0].kind is DocstringSectionKind.text


@pytest.mark.parametrize(
    "annotation",
    ["int", "Annotated[int, '']"],
)
def test_ignore_unannotated_yields(annotation: str) -> None:
    """Ignore yields that are not annotated with `Doc`."""
    with temporary_visited_package(
        "package",
        {
            "__init__.py": f"{typing_imports}\ndef f() -> Iterator[{annotation}]:\n    '''Docstring.'''",
        },
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        sections = package["f"].docstring.parsed
        assert len(sections) == 1
        assert sections[0].kind is DocstringSectionKind.text


@pytest.mark.parametrize(
    "annotation",
    ["int", "Annotated[int, '']"],
)
def test_ignore_unannotated_receives(annotation: str) -> None:
    """Ignore receives that are not annotated with `Doc`."""
    with temporary_visited_package(
        "package",
        {
            "__init__.py": f"{typing_imports}\ndef f() -> Generator[int, {annotation}, None]:\n    '''Docstring.'''",
        },
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        sections = package["f"].docstring.parsed
        assert len(sections) == 1
        assert sections[0].kind is DocstringSectionKind.text


def test_support_annotated_doc_package() -> None:
    """Test that the extension supports annotated-doc's Doc."""
    code = """
        from typing import Annotated
        from annotated_doc import Doc
        def hi(name: Annotated[str, Doc('Who to say hi to')]) -> None:
            '''Says hi.'''
            pass
    """
    with temporary_visited_package(
        "package",
        modules={"__init__.py": code},
        extensions=Extensions(TypingDocExtension()),
    ) as package:
        sections = package["hi"].docstring.parsed
        assert len(sections) == 2
        assert sections[1].kind is DocstringSectionKind.parameters
        assert sections[1].value[0].description == "Who to say hi to"
