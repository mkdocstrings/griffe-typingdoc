"""This module defines the Griffe TypingDoc extension."""

from __future__ import annotations

from typing import TYPE_CHECKING

from griffe import Docstring, Extension, Function, ObjectNode

from griffe_typingdoc import _dynamic, _static

if TYPE_CHECKING:
    import ast

    from griffe.dataclasses import Attribute
    from typing_extensions import Annotated, Doc  # type: ignore[attr-defined]


class TypingDocExtension(Extension):
    """Griffe extension that reads documentation from `typing.Doc`."""

    def on_attribute_instance(
        self,
        *,
        node: Annotated[
            ast.AST | ObjectNode,
            Doc("The object/AST node describing the attribute or its definition."),
        ],
        attr: Annotated[
            Attribute,
            Doc("The Griffe attribute just instantiated."),
        ],
    ) -> None:
        """Post-process Griffe attributes to create their docstring."""
        module = _dynamic if isinstance(node, ObjectNode) else _static

        new_sections = (
            docstring := module._attribute_docs(node, attr),
            deprecated_section := module._deprecated_docs(node, attr),
            raises_section := module._raises_docs(node, attr),
            warns_section := module._warns_docs(node, attr),
        )

        if not any(new_sections):
            return

        if not attr.docstring:
            attr.docstring = Docstring(docstring, parent=attr)

        sections = attr.docstring.parsed

        if deprecated_section := module._deprecated_docs(node, attr):
            sections.insert(0, deprecated_section)

        if raises_section := module._raises_docs(node, attr):
            sections.append(raises_section)

        if warns_section := module._warns_docs(node, attr):
            sections.append(warns_section)

    def on_function_instance(
        self,
        *,
        node: Annotated[
            ast.AST | ObjectNode,
            Doc("The object/AST node describing the function or its definition."),
        ],
        func: Annotated[
            Function,
            Doc(
                # Multiline docstring to test de-indentation.
                """
                The Griffe function just instantiated.
                """,
            ),
        ],
    ) -> None:
        """Post-process Griffe functions to add a parameters section."""
        module = _dynamic if isinstance(node, ObjectNode) else _static

        yields_section, receives_section, returns_section = module._yrr_docs(node, func)
        new_sections = (
            deprecated_section := module._deprecated_docs(node, func),
            params_section := module._parameters_docs(node, func),
            other_params_section := module._other_parameters_docs(node, func),
            warns_section := module._warns_docs(node, func),
            raises_section := module._raises_docs(node, func),
            yields_section,
            receives_section,
            returns_section,
        )

        if not any(new_sections):
            return

        if not func.docstring:
            func.docstring = Docstring("", parent=func)

        sections = func.docstring.parsed

        if other_params_section:
            sections.insert(1, other_params_section)

        if params_section:
            sections.insert(1, params_section)

        if deprecated_section:
            sections.insert(0, deprecated_section)

        if raises_section:
            sections.append(raises_section)

        if warns_section:
            sections.append(warns_section)

        if yields_section:
            sections.append(yields_section)

        if receives_section:
            sections.append(receives_section)

        if returns_section:
            sections.append(returns_section)
