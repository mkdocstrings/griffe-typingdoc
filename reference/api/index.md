# griffe_typingdoc

Griffe TypingDoc package.

Griffe extension for PEP 727 - Documentation Metadata in Typing.

Classes:

- **`TypingDocExtension`** – Griffe extension that reads documentation from typing.Doc.

## TypingDocExtension

```
TypingDocExtension()
```

Bases: `Extension`

Griffe extension that reads documentation from `typing.Doc`.

Methods:

- **`on_attribute_instance`** – Post-process Griffe attributes to create their docstring.
- **`on_function_instance`** – Post-process Griffe functions to add a parameters section.
- **`on_package`** – Post-process Griffe packages recursively (non-yet handled objects only).

Source code in `src/griffe_typingdoc/_internal/extension.py`

```
def __init__(self) -> None:
    self._handled: set[str] = set()
```

### on_attribute_instance

```
on_attribute_instance(
    *,
    node: Annotated[
        AST | ObjectNode,
        Doc(
            "The object/AST node describing the attribute or its definition."
        ),
    ],
    attr: Annotated[
        Attribute,
        Doc("The Griffe attribute just instantiated."),
    ],
    **kwargs: Any,
) -> None
```

Post-process Griffe attributes to create their docstring.

It applies only for dynamic analysis.

Parameters:

- **`node`** (`Annotated[AST | ObjectNode, Doc('The object/AST node describing the attribute or its definition.')]`) – The object/AST node describing the attribute or its definition.
- **`attr`** (`Annotated[Attribute, Doc('The Griffe attribute just instantiated.')]`) – The Griffe attribute just instantiated.

Source code in `src/griffe_typingdoc/_internal/extension.py`

```
def on_attribute_instance(
    self,
    *,
    node: Annotated[
        ast.AST | ObjectNode,
        Doc("The object/AST node describing the attribute or its definition."),
    ],
    attr: Annotated[
        Attribute,
        Doc("The Griffe attribute just instantiated."),
    ],
    **kwargs: Any,  # noqa: ARG002
) -> None:
    """Post-process Griffe attributes to create their docstring.

    It applies only for dynamic analysis.
    """
    if isinstance(node, ObjectNode):
        self._handle_attribute(attr, node=node)
```

### on_function_instance

```
on_function_instance(
    *,
    node: Annotated[
        AST | ObjectNode,
        Doc(
            "The object/AST node describing the function or its definition."
        ),
    ],
    func: Annotated[
        Function,
        Doc("The Griffe function just instantiated."),
    ],
    **kwargs: Any,
) -> None
```

Post-process Griffe functions to add a parameters section.

It applies only for dynamic analysis.

Parameters:

- **`node`** (`Annotated[AST | ObjectNode, Doc('The object/AST node describing the function or its definition.')]`) – The object/AST node describing the function or its definition.
- **`func`** (`Annotated[Function, Doc('The Griffe function just instantiated.')]`) – The Griffe function just instantiated.

Source code in `src/griffe_typingdoc/_internal/extension.py`

```
def on_function_instance(
    self,
    *,
    node: Annotated[
        ast.AST | ObjectNode,
        Doc("The object/AST node describing the function or its definition."),
    ],
    func: Annotated[
        Function,
        Doc("""The Griffe function just instantiated."""),
    ],
    **kwargs: Any,  # noqa: ARG002
) -> None:
    """Post-process Griffe functions to add a parameters section.

    It applies only for dynamic analysis.
    """
    if isinstance(node, ObjectNode):
        self._handle_function(func, node=node)
```

### on_package

```
on_package(
    *,
    pkg: Annotated[
        Module,
        Doc("The top-level module representing a package."),
    ],
    **kwargs: Any,
) -> None
```

Post-process Griffe packages recursively (non-yet handled objects only).

Parameters:

- **`pkg`** (`Annotated[Module, Doc('The top-level module representing a package.')]`) – The top-level module representing a package.

Source code in `src/griffe_typingdoc/_internal/extension.py`

```
def on_package(
    self,
    *,
    pkg: Annotated[
        Module,
        Doc("The top-level module representing a package."),
    ],
    **kwargs: Any,  # noqa: ARG002
) -> None:
    """Post-process Griffe packages recursively (non-yet handled objects only)."""
    self._handle_object(pkg)
```
