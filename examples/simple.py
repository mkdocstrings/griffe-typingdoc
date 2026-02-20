from __future__ import annotations

from typing import (
    Annotated,
    Generator,
    Iterator,
    NotRequired,
    TypedDict,
    Unpack,
    Doc,
)

# Documenting module/class attributes, replacing Attributes sections:
ATTRIBUTE: Annotated[
    str,
    Doc(
        """Showing off attributes.

        Supporting multiple lines.
        """
    )
]


# Documenting parameters, replacing Parameters sections:
def parameters(param1: Annotated[str, Doc("Description of param1.")] = "default"):
    """Showing off parameters."""


# Documenting other parameters (keyword arguments), replacing Other Parameters sections:
class OtherParameters(TypedDict, total=False):
    """Keyword arguments of [`simple.other_parameters`][]."""
    param1: Annotated[NotRequired[str], Doc("Description of param1.")]
    param2: Annotated[NotRequired[str], Doc("Description of param2.")]


def other_parameters(
    **kwargs: Annotated[Unpack[OtherParameters], Doc("See other parameters.")],  # noqa: ARG001
) -> None:
    """Showing off other parameters."""


# Documenting returned values, replacing Returns sections:
def return_value() -> Annotated[int, Doc("Returned integer.")]:
    """Showing off return values."""
    return 0


# Documenting yielded and received values, replacing Yields and Receives sections:
def generator() -> Generator[
    Annotated[int, Doc("Yielded integers.")],
    Annotated[int, Doc("Received integers.")],
    Annotated[int, Doc("Final returned value.")],
]:
    """Showing off generators."""


# Same thing with Iterator instead of Generator:
def iterator() -> Iterator[Annotated[int, Doc("Yielded integers.")]]:
    """Showing off iterators."""


# Advanced use-case: documenting multiple yielded/received/returned values:
def return_tuple() -> Generator[
    tuple[
        Annotated[int, Doc("First element of the yielded value.")],
        Annotated[float, Doc("Second element of the yielded value.")],
    ],
    tuple[
        Annotated[int, Doc("First element of the received value.")],
        Annotated[float, Doc("Second element of the received value.")],
    ],
    tuple[
        Annotated[int, Doc("First element of the returned value.")],
        Annotated[float, Doc("Second element of the returned value.")],
    ],
]:
    """Showing off tuples as yield/receive/return values."""
