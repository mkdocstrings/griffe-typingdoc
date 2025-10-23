# Helpers to get documentation metadata statically.

from __future__ import annotations

import inspect
from ast import literal_eval
from collections import defaultdict
from typing import TYPE_CHECKING, Any

from griffe import Expr, ExprCall, ExprSubscript, ExprTuple, ParameterKind

from griffe_typingdoc._internal.docstrings import (
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
    from collections.abc import Sequence

    from griffe import (
        Attribute,
        DocstringSectionAdmonition,
        DocstringSectionParameters,
        DocstringSectionRaises,
        DocstringSectionReceives,
        DocstringSectionReturns,
        DocstringSectionWarns,
        DocstringSectionYields,
        Function,
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
    "annotated_doc.Doc": _set_metadata_doc,
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


def _attribute_docs(attr: Attribute, **kwargs: Any) -> str:  # noqa: ARG001
    return _metadata(attr.annotation).get("doc", "")


def _parameters_docs(func: Function, **kwargs: Any) -> DocstringSectionParameters | None:  # noqa: ARG001
    params_data: dict[str, dict[str, Any]] = defaultdict(dict)
    for parameter in _no_self_params(func):
        stars = {ParameterKind.var_positional: "*", ParameterKind.var_keyword: "**"}.get(parameter.kind, "")  # type: ignore[arg-type]
        param_name = f"{stars}{parameter.name}"
        metadata = _metadata(parameter.annotation)
        if "deprecated" in metadata or "doc" in metadata:
            description = f"{metadata.get('deprecated', '')} {metadata.get('doc', '')}".lstrip()
            params_data[param_name]["description"] = description
            params_data[param_name]["annotation"] = parameter.annotation
    if params_data:
        return _to_parameters_section(params_data, func)
    return None


def _other_parameters_docs(func: Function, **kwargs: Any) -> DocstringSectionParameters | None:  # noqa: ARG001
    for parameter in func.parameters:
        if parameter.kind is ParameterKind.var_keyword:
            annotation = parameter.annotation
            if isinstance(annotation, ExprSubscript) and annotation.canonical_path in {
                "typing.Annotated",
                "typing_extensions.Annotated",
            }:
                annotation = annotation.slice.elements[0]  # type: ignore[union-attr]
            if isinstance(annotation, ExprSubscript) and annotation.canonical_path in {
                "typing.Unpack",
                "typing_extensions.Unpack",
            }:
                slice_path = annotation.slice.canonical_path  # type: ignore[union-attr]
                typed_dict = func.modules_collection[slice_path]
                params_data = {
                    attr.name: {"annotation": attr.annotation, "description": description}
                    for attr in typed_dict.members.values()
                    if (description := _metadata(attr.annotation).get("doc")) is not None
                }
                if params_data:
                    return _to_other_parameters_section(params_data)
            break
    return None


def _yields_docs(func: Function, **kwargs: Any) -> DocstringSectionYields | None:  # noqa: ARG001
    yield_annotation = None
    annotation = func.returns

    if isinstance(annotation, ExprSubscript):
        if annotation.canonical_path in {"typing.Generator", "typing_extensions.Generator"}:
            yield_annotation = annotation.slice.elements[0]  # type: ignore[union-attr]
        elif annotation.canonical_path in {"typing.Iterator", "typing_extensions.Iterator"}:
            yield_annotation = annotation.slice

    if yield_annotation:
        if isinstance(yield_annotation, ExprSubscript) and yield_annotation.is_tuple:
            yield_elements = yield_annotation.slice.elements  # type: ignore[union-attr]
        else:
            yield_elements = [yield_annotation]
        yield_data = [
            {"annotation": element, **metadata}
            for element in yield_elements
            if "doc" in (metadata := _metadata(element))
        ]
        if yield_data:
            return _to_yields_section(yield_data)

    return None


def _receives_docs(func: Function, **kwargs: Any) -> DocstringSectionReceives | None:  # noqa: ARG001
    receive_annotation = None
    annotation = func.returns

    if isinstance(annotation, ExprSubscript) and annotation.canonical_path in {
        "typing.Generator",
        "typing_extensions.Generator",
    }:
        receive_annotation = annotation.slice.elements[1]  # type: ignore[union-attr]

    if receive_annotation:
        if isinstance(receive_annotation, ExprSubscript) and receive_annotation.is_tuple:
            receive_elements = receive_annotation.slice.elements  # type: ignore[union-attr]
        else:
            receive_elements = [receive_annotation]
        receive_data = [
            {"annotation": element, **metadata}
            for element in receive_elements
            if "doc" in (metadata := _metadata(element))
        ]
        if receive_data:
            return _to_receives_section(receive_data)

    return None


def _returns_docs(func: Function, **kwargs: Any) -> DocstringSectionReturns | None:  # noqa: ARG001
    return_annotation = None
    annotation = func.returns

    if isinstance(annotation, ExprSubscript) and annotation.canonical_path in {
        "typing.Generator",
        "typing_extensions.Generator",
    }:
        return_annotation = annotation.slice.elements[2]  # type: ignore[union-attr]
    elif isinstance(annotation, ExprSubscript) and annotation.canonical_path in {
        "typing.Annotated",
        "typing_extensions.Annotated",
    }:
        return_annotation = annotation

    if return_annotation:
        if isinstance(return_annotation, ExprSubscript) and return_annotation.is_tuple:
            return_elements = return_annotation.slice.elements  # type: ignore[union-attr]
        else:
            return_elements = [return_annotation]
        return_data = [
            {"annotation": element, **metadata}
            for element in return_elements
            if "doc" in (metadata := _metadata(element))
        ]
        if return_data:
            return _to_returns_section(return_data)

    return None


def _warns_docs(attr_or_func: Attribute | Function, **kwargs: Any) -> DocstringSectionWarns | None:  # noqa: ARG001
    if attr_or_func.is_attribute:
        annotation = attr_or_func.annotation
    elif attr_or_func.is_function:
        annotation = attr_or_func.returns  # type: ignore[union-attr]
    else:
        return None
    metadata = _metadata(annotation)
    if metadata["warns"]:
        return _to_warns_section({"annotation": warned[0], "description": warned[1]} for warned in metadata["warns"])
    return None


def _raises_docs(attr_or_func: Attribute | Function, **kwargs: Any) -> DocstringSectionRaises | None:  # noqa: ARG001
    if attr_or_func.is_attribute:
        annotation = attr_or_func.annotation
    elif attr_or_func.is_function:
        annotation = attr_or_func.returns  # type: ignore[union-attr]
    else:
        return None
    metadata = _metadata(annotation)
    if metadata["raises"]:
        return _to_raises_section({"annotation": raised[0], "description": raised[1]} for raised in metadata["raises"])
    return None


def _deprecated_docs(
    attr_or_func: Attribute | Function,
    **kwargs: Any,  # noqa: ARG001
) -> DocstringSectionAdmonition | None:
    if attr_or_func.is_attribute:
        annotation = attr_or_func.annotation
    elif attr_or_func.is_function:
        annotation = attr_or_func.returns  # type: ignore[union-attr]
    else:
        return None
    metadata = _metadata(annotation)
    if "deprecated" in metadata:
        return _to_deprecated_section({"description": metadata["deprecated"]})
    return None
