"""This module defines an alternate form of the `typing.doc` function.

See https://github.com/tiangolo/fastapi/blob/typing-doc/typing_doc.md#alternate-form.
"""

from __future__ import annotations

from typing import Any, Callable, Mapping, TypeVar

_Type = TypeVar("_Type")


def __typing_doc__(  # noqa: N807
    *,
    description: str | None = None,  # noqa: ARG001
    deprecated: bool = False,  # noqa: ARG001
    discouraged: bool = False,  # noqa: ARG001
    raises: Mapping[type[BaseException], str | None] | None = None,  # noqa: ARG001
    extra: dict[Any, Any] | None = None,  # noqa: ARG001
) -> Callable[[_Type], _Type]:
    return lambda _: _
