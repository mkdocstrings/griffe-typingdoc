"""This module defines an alternate form of the `typing.doc` function.

See https://github.com/tiangolo/fastapi/blob/typing-doc/typing_doc.md#alternate-form.
"""

from __future__ import annotations

from typing import Any, Callable, Mapping, TypeVar

_Type = TypeVar("_Type")


def __typing_doc__(  # noqa: N807
    *,
    description: str | None = None,
    deprecated: bool = False,
    discouraged: bool = False,
    raises: Mapping[type[BaseException], str | None] | None = None,
    extra: dict[Any, Any] | None = None,
) -> Callable[[_Type], _Type]:
    return lambda _: _
