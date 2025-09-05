# Helpers to build docstring sections.

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from griffe import (
    DocstringParameter,
    DocstringRaise,
    DocstringReceive,
    DocstringReturn,
    DocstringSectionAdmonition,
    DocstringSectionOtherParameters,
    DocstringSectionParameters,
    DocstringSectionRaises,
    DocstringSectionReceives,
    DocstringSectionReturns,
    DocstringSectionWarns,
    DocstringSectionYields,
    DocstringWarn,
    DocstringYield,
)

if TYPE_CHECKING:
    from collections.abc import Iterable

    from griffe import Function, Parameter


def _no_self_params(func: Function) -> list[Parameter]:
    if func.parent and func.parent.is_class and func.parameters and func.parameters[0].name in {"self", "cls"}:
        return list(func.parameters)[1:]
    return list(func.parameters)


def _to_parameters_section(params_dict: dict[str, dict[str, Any]], func: Function) -> DocstringSectionParameters:
    return DocstringSectionParameters(
        [
            DocstringParameter(
                name=param_name,
                description=param_doc["description"],
                annotation=param_doc["annotation"],
                value=func.parameters[param_name].default,
            )
            for param_name, param_doc in params_dict.items()
        ],
    )


def _to_other_parameters_section(params_dict: dict[str, dict[str, Any]]) -> DocstringSectionOtherParameters:
    return DocstringSectionOtherParameters(
        [
            DocstringParameter(
                name=param_name,
                description=param_doc["description"],
                annotation=param_doc["annotation"],
            )
            for param_name, param_doc in params_dict.items()
        ],
    )


def _to_yields_section(yield_data: Iterable[dict[str, Any]]) -> DocstringSectionYields:
    return DocstringSectionYields(
        [
            DocstringYield(
                name=yield_dict.get("name", ""),
                description=yield_dict.get("doc", ""),
                annotation=yield_dict["annotation"],
            )
            for yield_dict in yield_data
        ],
    )


def _to_receives_section(receive_data: Iterable[dict[str, Any]]) -> DocstringSectionReceives:
    return DocstringSectionReceives(
        [
            DocstringReceive(
                name=receive_dict.get("name", ""),
                description=receive_dict.get("doc", ""),
                annotation=receive_dict["annotation"],
            )
            for receive_dict in receive_data
        ],
    )


def _to_returns_section(return_data: Iterable[dict[str, Any]]) -> DocstringSectionReturns:
    return DocstringSectionReturns(
        [
            DocstringReturn(
                name=return_dict.get("name", ""),
                description=return_dict.get("doc", ""),
                annotation=return_dict["annotation"],
            )
            for return_dict in return_data
        ],
    )


def _to_warns_section(warn_data: Iterable[dict[str, Any]]) -> DocstringSectionWarns:
    return DocstringSectionWarns(
        [
            DocstringWarn(
                annotation=warn_dict["annotation"],
                description=warn_dict.get("description", ""),
            )
            for warn_dict in warn_data
        ],
    )


def _to_raises_section(raise_data: Iterable[dict[str, Any]]) -> DocstringSectionRaises:
    return DocstringSectionRaises(
        [
            DocstringRaise(
                annotation=raise_dict["annotation"],
                description=raise_dict.get("description", ""),
            )
            for raise_dict in raise_data
        ],
    )


def _to_deprecated_section(deprecation_data: dict[str, Any]) -> DocstringSectionAdmonition:
    description = deprecation_data["description"]
    description_lines = deprecation_data["description"].split("\n")
    if len(description_lines) > 1:
        title = description_lines[0].strip()
        description = "\n".join(description_lines[1:]).strip()
    else:
        title = description
        description = ""
    return DocstringSectionAdmonition(kind="danger", title=title, text=description)
