"""This module defines the Griffe TypingDoc extension."""

from __future__ import annotations

from ast import literal_eval
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Sequence

from griffe import Docstring, Extension, Function, ObjectNode
from griffe.docstrings.dataclasses import DocstringParameter, DocstringSectionParameters
from griffe.expressions import Expr, ExprCall, ExprSubscript, ExprTuple
from typing_extensions import get_type_hints

if TYPE_CHECKING:
    import ast

    from typing_extensions import Annotated, doc  # type: ignore[attr-defined]


class TypingDocExtension(Extension):
    """Griffe extension that reads documentation from `typing.doc`."""

    def on_function_instance(
        self,
        node: Annotated[
            ast.AST | ObjectNode,
            doc("The object/AST node describing the function or its definition."),
        ],
        func: Annotated[
            Function,
            doc("The Griffe function just instantiated."),
        ],
    ) -> None:
        """Post-process Griffe functions to add a parameters section."""
        if isinstance(node, ObjectNode):
            hints = get_type_hints(node.obj, include_extras=True)
            params_doc: dict[str, dict[str, Any]] = {
                name: {"description": param.__metadata__[0].documentation}
                for name, param in hints.items()
                if name != "return"
            }
        else:
            params_doc = defaultdict(dict)
            for parameter in func.parameters:
                annotation = parameter.annotation
                if isinstance(annotation, ExprSubscript) and annotation.left.canonical_path in {
                    "typing.Annotated",
                    "typing_extensions.Annotated",
                }:
                    metadata: Sequence[str | Expr]
                    if isinstance(annotation.slice, ExprTuple):
                        annotation, *metadata = annotation.slice.elements
                    else:
                        annotation = annotation.slice
                        metadata = ()
                    doc = None
                    for data in metadata:
                        if isinstance(data, ExprCall) and data.function.canonical_path in {
                            "typing.doc",
                            "typing_extensions.doc",
                        }:
                            doc = literal_eval(str(data.arguments[0]))
                    params_doc[parameter.name]["annotation"] = annotation
                    if doc:
                        params_doc[parameter.name]["description"] = doc

        if params_doc:
            if not func.docstring:
                func.docstring = Docstring("", parent=func)
            sections = func.docstring.parsed
            param_section = DocstringSectionParameters(
                [
                    DocstringParameter(
                        name=param_name,
                        description=param_doc["description"],
                        annotation=param_doc["annotation"],
                        value=func.parameters[param_name].default,  # type: ignore[arg-type]
                    )
                    for param_name, param_doc in params_doc.items()
                ],
            )
            sections.insert(1, param_section)
