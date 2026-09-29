# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2023, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Helpers to get documentation metadata dynamically.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, get_type_hints

from griffe_typingdoc._internal.docstrings import _to_parameters_section

if TYPE_CHECKING:
    from griffe import (
        Attribute,
        DocstringSectionAdmonition,
        DocstringSectionOtherParameters,
        DocstringSectionParameters,
        DocstringSectionRaises,
        DocstringSectionReceives,
        DocstringSectionReturns,
        DocstringSectionWarns,
        DocstringSectionYields,
        Function,
        ObjectNode,
    )


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


def _attribute_docs(attr: Attribute, *, node: ObjectNode, **kwargs: Any) -> str:  # noqa: ARG001
    return _doc(attr.name, _hints(node)) or ""


def _parameters_docs(
    func: Function,
    *,
    node: ObjectNode,
    **kwargs: Any,  # noqa: ARG001
) -> DocstringSectionParameters | None:
    hints = _hints(node)
    params_doc: dict[str, dict[str, Any]] = {
        name: {"description": _doc(name, hints)} for name in hints if name != "return"
    }
    if params_doc:
        return _to_parameters_section(params_doc, func)
    return None


# FIXME: Implement this function.
def _other_parameters_docs(
    func: Function,  # noqa: ARG001
    *,
    node: ObjectNode,  # noqa: ARG001
    **kwargs: Any,  # noqa: ARG001
) -> DocstringSectionOtherParameters | None:
    return None


# FIXME: Implement this function.
def _deprecated_docs(
    attr_or_func: Attribute | Function,  # noqa: ARG001
    *,
    node: ObjectNode,  # noqa: ARG001
    **kwargs: Any,  # noqa: ARG001
) -> DocstringSectionAdmonition | None:
    return None


# FIXME: Implement this function.
def _raises_docs(
    attr_or_func: Attribute | Function,  # noqa: ARG001
    *,
    node: ObjectNode,  # noqa: ARG001
    **kwargs: Any,  # noqa: ARG001
) -> DocstringSectionRaises | None:
    return None


# FIXME: Implement this function.
def _warns_docs(
    attr_or_func: Attribute | Function,  # noqa: ARG001
    *,
    node: ObjectNode,  # noqa: ARG001
    **kwargs: Any,  # noqa: ARG001
) -> DocstringSectionWarns | None:
    return None


# FIXME: Implement this function.
def _yields_docs(
    func: Function,  # noqa: ARG001
    *,
    node: ObjectNode,  # noqa: ARG001
    **kwargs: Any,  # noqa: ARG001
) -> DocstringSectionYields | None:
    return None


# FIXME: Implement this function.
def _receives_docs(
    func: Function,  # noqa: ARG001
    *,
    node: ObjectNode,  # noqa: ARG001
    **kwargs: Any,  # noqa: ARG001
) -> DocstringSectionReceives | None:
    return None


# FIXME: Implement this function.
def _returns_docs(
    func: Function,  # noqa: ARG001
    *,
    node: ObjectNode,  # noqa: ARG001
    **kwargs: Any,  # noqa: ARG001
) -> DocstringSectionReturns | None:
    return None
