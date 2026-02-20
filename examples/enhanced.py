# This gist shows how we could get rid of docstrings micro-syntax
# like Google-style and Numpydoc-style pseudo-standards,
# using an enhanced version of PEP 727.

# The goal is to replace the following sections:

# deprecated
# Parameters
# Other Parameters
# Raises
# Warns
# Yields
# Receives
# Returns

from __future__ import annotations

from typing import (
    Annotated,
    Generator,
    deprecated,
    Doc,
    Name,
    Raises,
    Warns,
)


# Documenting deprecations, replacing Deprecated sections:
DEPRECATED: Annotated[
    int,
    deprecated(
        """Deprecated since v2.

        Please stop using this deprecated attribute, thanks!
        """
    ),
    Doc("Showing off deprecated attributes."),
]


# For functions, maybe add the information to the return value annotation:
def deprecated1() -> Annotated[None, deprecated("Deprecated since v2.")]:
    """Showing off deprecated functions."""


# For parameters:
def deprecated2(param1: Annotated[int, deprecated("Deprecated since v2."), Doc("Description of param1.")] = 0):
    """Showing off deprecated parameters."""


# Documenting exceptions, replacing Raises sections,
# maybe add the information to the return value annotation:
def exceptions() -> (
    Annotated[
        None,
        Raises(ValueError, "When something goes wrong."),
        Raises(TypeError, "When something goes even wronger."),
    ]
):
    """Showing off raised exceptions."""


# Documenting warnings, replacing Warns sections,
# maybe add the information to the return value annotation:
def warnings() -> (
    Annotated[
        None,
        Warns(FutureWarning, "Hello users."),
        Warns(DeprecationWarning, "Hello developers."),
    ]
):
    """Showing off emitted warnings."""


# Advanced use-case: documenting multiple yielded/received/returned values:
def return_tuple() -> (
    Generator[
        tuple[
            Annotated[int, Name("python"), Doc("First element of the yielded value.")],
            Annotated[float, Name("cobra"), Doc("Second element of the yielded value.")],
        ],
        tuple[
            Annotated[int, Name("beep"), Doc("First element of the received value.")],
            Annotated[float, Name("boop"), Doc("Second element of the received value.")],
        ],
        tuple[
            Annotated[int, Name("super"), Doc("First element of the returned value.")],
            Annotated[float, Name("hyper"), Doc("Second element of the returned value.")],
        ],
    ]
):
    """Showing off tuples as yield/receive/return values."""
