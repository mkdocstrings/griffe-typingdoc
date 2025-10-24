"""Griffe TypingDoc package.

Griffe extension for `annotated-doc` (originally PEP 727):

> Document parameters, class attributes, return types, and variables inline, with Annotated.
"""

# TODO: Set parameter docstrings?

from __future__ import annotations

from griffe_typingdoc._internal.extension import TypingDocExtension

__all__: list[str] = ["TypingDocExtension"]
