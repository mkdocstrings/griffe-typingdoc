"""Helpers to get documentation metadata dynamically."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from typing_extensions import get_type_hints

from griffe_typingdoc._docstrings import _to_parameters_section

if TYPE_CHECKING:
    from griffe import Attribute, Function, ObjectNode
    from griffe.docstrings.dataclasses import DocstringSectionParameters


def _hints(node: ObjectNode) -> dict[str, str]:
    try:
        return get_type_hints(node.obj, include_extras=True)
    except TypeError:
        if node.parent:
            return _hints(node.parent)
    return {}


def _doc(name: str, hints: dict[str, Any]) -> str | None:
    try:
        return hints[name].__metadata__[0].documentation
    except (AttributeError, KeyError):
        return None


def _attribute_docs(node: ObjectNode, attr: Attribute) -> str:
    return _doc(attr.name, _hints(node)) or ""


def _parameters_docs(node: ObjectNode, func: Function) -> DocstringSectionParameters | None:
    hints = _hints(node)
    params_doc: dict[str, dict[str, Any]] = {
        name: {"description": _doc(name, hints)} for name in hints if name != "return"
    }
    if params_doc:
        return _to_parameters_section(params_doc, func)
    return None
