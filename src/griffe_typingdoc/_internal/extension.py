# This module defines the Griffe TypingDoc extension.

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from griffe import Alias, Docstring, Extension, Function, ObjectNode

from griffe_typingdoc._internal import dynamic, static

if TYPE_CHECKING:
    import ast
    from typing import Annotated

    from griffe import Attribute, Module, Object
    from typing_extensions import Doc


class TypingDocExtension(Extension):
    """Griffe extension that reads documentation from `typing.Doc`."""

    def __init__(self) -> None:
        self._handled: set[str] = set()

    def _handle_attribute(self, attr: Attribute, /, *, node: ObjectNode | None = None) -> None:
        if attr.path in self._handled:
            return
        self._handled.add(attr.path)

        module = dynamic if node else static

        new_sections = (
            docstring := module._attribute_docs(attr, node=node),
            deprecated_section := module._deprecated_docs(attr, node=node),
            raises_section := module._raises_docs(attr, node=node),
            warns_section := module._warns_docs(attr, node=node),
        )

        if not any(new_sections):
            return

        if not attr.docstring:
            attr.docstring = Docstring(docstring, parent=attr)

        sections = attr.docstring.parsed

        if deprecated_section:
            sections.insert(0, deprecated_section)

        if raises_section:
            sections.append(raises_section)

        if warns_section:
            sections.append(warns_section)

    def _handle_function(self, func: Function, /, *, node: ObjectNode | None = None) -> None:
        if func.path in self._handled:
            return
        self._handled.add(func.path)

        module = dynamic if node else static

        new_sections = (
            deprecated_section := module._deprecated_docs(func, node=node),
            params_section := module._parameters_docs(func, node=node),
            other_params_section := module._other_parameters_docs(func, node=node),
            warns_section := module._warns_docs(func, node=node),
            raises_section := module._raises_docs(func, node=node),
            yields_section := module._yields_docs(func, node=node),
            receives_section := module._receives_docs(func, node=node),
            returns_section := module._returns_docs(func, node=node),
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

    def _handle_object(self, obj: Object | Alias) -> None:
        if obj.is_alias:
            return
        if obj.is_module or obj.is_class:
            for member in obj.members.values():
                self._handle_object(member)
        elif obj.is_function:
            self._handle_function(obj)  # type: ignore[arg-type]
        elif obj.is_attribute:
            self._handle_attribute(obj)  # type: ignore[arg-type]

    def on_package(
        self,
        *,
        pkg: Annotated[
            Module,
            Doc("The top-level module representing a package."),
        ],
        **kwargs: Any,  # noqa: ARG002
    ) -> None:
        """Post-process Griffe packages recursively (non-yet handled objects only)."""
        self._handle_object(pkg)

    def on_function_instance(
        self,
        *,
        node: Annotated[
            ast.AST | ObjectNode,
            Doc("The object/AST node describing the function or its definition."),
        ],
        func: Annotated[
            Function,
            Doc("""The Griffe function just instantiated."""),
        ],
        **kwargs: Any,  # noqa: ARG002
    ) -> None:
        """Post-process Griffe functions to add a parameters section.

        It applies only for dynamic analysis.
        """
        if isinstance(node, ObjectNode):
            self._handle_function(func, node=node)

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
        **kwargs: Any,  # noqa: ARG002
    ) -> None:
        """Post-process Griffe attributes to create their docstring.

        It applies only for dynamic analysis.
        """
        if isinstance(node, ObjectNode):
            self._handle_attribute(attr, node=node)
