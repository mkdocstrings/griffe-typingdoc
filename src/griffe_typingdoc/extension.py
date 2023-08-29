"""This module defines the Griffe TypingDoc extension."""

from __future__ import annotations

import ast
from collections import defaultdict
from typing import TYPE_CHECKING, Annotated, Any

from griffe.agents.extensions import VisitorExtension, When
from griffe.agents.nodes import safe_get_annotation
from griffe.docstrings.dataclasses import DocstringParameter, DocstringSectionParameters

from griffe_typingdoc.typing_doc import __typing_doc__

if TYPE_CHECKING:
    from griffe.dataclasses import Function


@__typing_doc__(description="Griffe extension parsing the `typing.doc` decorator.")
class TypingDocExtension(VisitorExtension):
    """Griffe extension parsing the `typing.doc` decorator."""

    when = When.after_all

    @__typing_doc__(description="Visit a function definition.")
    def visit_functiondef(
        self,
        node: Annotated[
            ast.FunctionDef,
            __typing_doc__(
                description="The AST node describing the function definition.",
            ),
        ],
    ) -> None:
        """Visit a function definition.

        This function takes a function definition node and visits its contents,
        particularly its decorators, to build up the documentation metadata.
        """
        func: Function = self.visitor.current.members[node.name]  # type: ignore[assignment]

        func_doc = {}
        for decorator_node in node.decorator_list:
            if isinstance(decorator_node, ast.Call) and decorator_node.func.id == "__typing_doc__":  # type: ignore[attr-defined]
                func_doc.update({kw.arg: kw.value.value for kw in decorator_node.keywords})  # type: ignore[attr-defined]

        params_doc: dict[str, dict[str, Any]] = defaultdict(dict)
        for arg in node.args.args:
            if isinstance(arg.annotation, ast.Subscript) and arg.annotation.value.id == "Annotated":  # type: ignore[attr-defined]
                param_name = arg.arg
                params_doc[param_name]["annotation"] = safe_get_annotation(
                    arg.annotation.slice.elts[0],  # type: ignore[attr-defined]
                    func.parent,
                )
                doc = arg.annotation.slice.elts[1]  # type: ignore[attr-defined]
                if isinstance(doc, ast.Call) and doc.func.id == "__typing_doc__":  # type: ignore[attr-defined]
                    params_doc[param_name].update({kw.arg: kw.value.value for kw in doc.keywords})  # type: ignore[attr-defined,misc]

        if (func_doc or params_doc) and func.docstring:
            sections = func.docstring.parsed
            if params_doc:
                docstring_params = []
                for param_name, param_doc in params_doc.items():
                    docstring_params.append(
                        DocstringParameter(
                            name=param_name,
                            description=param_doc["description"],
                            annotation=param_doc["annotation"],
                            value=func.parameters[param_name].default,  # type: ignore[arg-type]
                        ),
                    )
                sections.append(DocstringSectionParameters(docstring_params))
