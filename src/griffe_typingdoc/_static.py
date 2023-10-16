"""Helpers to get documentation metadata statically."""

from __future__ import annotations

import inspect
from ast import literal_eval
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Sequence

from griffe.enumerations import ParameterKind
from griffe.expressions import Expr, ExprCall, ExprSubscript, ExprTuple

from griffe_typingdoc._docstrings import (
    _no_self_params,
    _to_deprecated_section,
    _to_other_parameters_section,
    _to_parameters_section,
    _to_raises_section,
    _to_receives_section,
    _to_returns_section,
    _to_warns_section,
    _to_yields_section,
)

if TYPE_CHECKING:
    import ast

    from griffe import Function
    from griffe.dataclasses import Attribute
    from griffe.docstrings.dataclasses import (
        DocstringSectionAdmonition,
        DocstringSectionParameters,
        DocstringSectionRaises,
        DocstringSectionReceives,
        DocstringSectionReturns,
        DocstringSectionWarns,
        DocstringSectionYields,
    )


def _literal(value: str | Expr) -> str:
    return inspect.cleandoc(literal_eval(str(value)))


def _set_metadata_doc(metadata: dict[str, Any], data: ExprCall) -> None:
    metadata["doc"] = _literal(data.arguments[0])


def _set_metadata_deprecated(metadata: dict[str, Any], data: ExprCall) -> None:
    metadata["deprecated"] = _literal(data.arguments[0])


def _set_metadata_name(metadata: dict[str, Any], data: ExprCall) -> None:
    metadata["name"] = _literal(data.arguments[0])


def _set_metadata_raises(metadata: dict[str, Any], data: ExprCall) -> None:
    metadata["raises"].append((data.arguments[0], _literal(data.arguments[1])))


def _set_metadata_warns(metadata: dict[str, Any], data: ExprCall) -> None:
    metadata["warns"].append((data.arguments[0], _literal(data.arguments[1])))


_set_metadata_map = {
    "typing.Doc": _set_metadata_doc,
    "typing_extensions.Doc": _set_metadata_doc,
    "typing.deprecated": _set_metadata_deprecated,
    "typing_extensions.deprecated": _set_metadata_deprecated,
    "typing.Name": _set_metadata_name,
    "typing_extensions.Name": _set_metadata_name,
    "typing.Raises": _set_metadata_raises,
    "typing_extensions.Raises": _set_metadata_raises,
    "typing.Warns": _set_metadata_warns,
    "typing_extensions.Warns": _set_metadata_warns,
}


def _set_metadata(metadata: dict[str, Any], data: ExprCall) -> None:
    if data.function.canonical_path in _set_metadata_map:
        _set_metadata_map[data.function.canonical_path](metadata, data)


def _metadata(annotation: str | Expr | None) -> dict[str, Any]:
    metadata: dict[str, Any] = {"raises": [], "warns": []}
    if isinstance(annotation, ExprSubscript) and annotation.canonical_path in {
        "typing.Annotated",
        "typing_extensions.Annotated",
    }:
        annotated_data: Sequence[str | Expr]
        if isinstance(annotation.slice, ExprTuple):
            annotation, *annotated_data = annotation.slice.elements
        else:
            annotation = annotation.slice
            annotated_data = ()
        for data in annotated_data:
            if isinstance(data, ExprCall):
                _set_metadata(metadata, data)
    return metadata


def _attribute_docs(node: ast.AST, attr: Attribute) -> str:  # noqa: ARG001
    return _metadata(attr.annotation).get("doc", "")


def _parameters_docs(node: ast.AST, func: Function) -> DocstringSectionParameters | None:  # noqa: ARG001
    params_doc: dict[str, dict[str, Any]] = defaultdict(dict)
    for parameter in _no_self_params(func):
        stars = {ParameterKind.var_positional: "*", ParameterKind.var_keyword: "**"}.get(parameter.kind, "")  # type: ignore[arg-type]
        param_name = f"{stars}{parameter.name}"
        metadata = _metadata(parameter.annotation)
        description = f'{metadata.get("deprecated", "")} {metadata.get("doc", "")}'.lstrip()
        params_doc[param_name]["annotation"] = parameter.annotation
        params_doc[param_name]["description"] = description
    if params_doc:
        return _to_parameters_section(params_doc, func)
    return None


def _other_parameters_docs(node: ast.AST, func: Function) -> DocstringSectionParameters | None:  # noqa: ARG001
    for parameter in func.parameters:
        if parameter.kind is ParameterKind.var_keyword:
            annotation = parameter.annotation
            if isinstance(annotation, ExprSubscript) and annotation.canonical_path in {
                "typing.Annotated",
                "typing_extensions.Annotated",
            }:
                annotation = annotation.slice.elements[0]  # type: ignore[attr-defined]
            if isinstance(annotation, ExprSubscript) and annotation.canonical_path in {
                "typing.Unpack",
                "typing_extensions.Unpack",
            }:
                typed_dict = annotation.slice.parent.get_member(annotation.slice.name)  # type: ignore[attr-defined]
                params_doc = {
                    attr.name: {"annotation": attr.annotation, "description": _metadata(attr.annotation).get("doc", "")}
                    for attr in typed_dict.members.values()
                }
                if params_doc:
                    return _to_other_parameters_section(params_doc)
            break
    return None


def _yrr_docs(
    node: ast.AST,  # noqa: ARG001
    func: Function,
) -> tuple[DocstringSectionYields | None, DocstringSectionReceives | None, DocstringSectionReturns | None]:
    yields_section = None
    receives_section = None
    returns_section = None

    annotation = func.returns

    yield_annotation = None
    receive_annotation = None
    return_annotation = None

    if isinstance(annotation, ExprSubscript):
        if annotation.canonical_path in {"typing.Generator", "typing_extensions.Generator"}:
            yield_annotation = annotation.slice.elements[0]  # type: ignore[attr-defined]
            receive_annotation = annotation.slice.elements[1]  # type: ignore[attr-defined]
            return_annotation = annotation.slice.elements[2]  # type: ignore[attr-defined]
        elif annotation.canonical_path in {"typing.Iterator", "typing_extensions.Iterator"}:
            yield_annotation = annotation.slice

    if yield_annotation:
        if isinstance(yield_annotation, ExprSubscript) and yield_annotation.is_tuple:
            yield_elements = yield_annotation.slice.elements  # type: ignore[attr-defined]
        else:
            yield_elements = [yield_annotation]
        yields_section = _to_yields_section({"annotation": element, **_metadata(element)} for element in yield_elements)

    if receive_annotation:
        if isinstance(receive_annotation, ExprSubscript) and receive_annotation.is_tuple:
            receive_elements = receive_annotation.slice.elements  # type: ignore[attr-defined]
        else:
            receive_elements = [receive_annotation]
        receives_section = _to_receives_section(
            {"annotation": element, **_metadata(element)} for element in receive_elements
        )

    if return_annotation:
        if isinstance(return_annotation, ExprSubscript) and return_annotation.is_tuple:
            return_elements = return_annotation.slice.elements  # type: ignore[attr-defined]
        else:
            return_elements = [return_annotation]
        returns_section = _to_returns_section(
            {"annotation": element, **_metadata(element)} for element in return_elements
        )

    return yields_section, receives_section, returns_section


def _warns_docs(node: ast.AST, attr_or_func: Attribute | Function) -> DocstringSectionWarns | None:  # noqa: ARG001
    if attr_or_func.is_attribute:
        annotation = attr_or_func.annotation
    elif attr_or_func.is_function:
        annotation = attr_or_func.returns  # type: ignore[union-attr]
    metadata = _metadata(annotation)
    if metadata["warns"]:
        return _to_warns_section({"annotation": warned[0], "description": warned[1]} for warned in metadata["warns"])
    return None


def _raises_docs(node: ast.AST, attr_or_func: Attribute | Function) -> DocstringSectionRaises | None:  # noqa: ARG001
    if attr_or_func.is_attribute:
        annotation = attr_or_func.annotation
    elif attr_or_func.is_function:
        annotation = attr_or_func.returns  # type: ignore[union-attr]
    metadata = _metadata(annotation)
    if metadata["raises"]:
        return _to_raises_section({"annotation": raised[0], "description": raised[1]} for raised in metadata["raises"])
    return None


def _deprecated_docs(
    node: ast.AST,  # noqa: ARG001
    attr_or_func: Attribute | Function,
) -> DocstringSectionAdmonition | None:
    if attr_or_func.is_attribute:
        annotation = attr_or_func.annotation
    elif attr_or_func.is_function:
        annotation = attr_or_func.returns  # type: ignore[union-attr]
    metadata = _metadata(annotation)
    if "deprecated" in metadata:
        return _to_deprecated_section({"description": metadata["deprecated"]})
    return None
