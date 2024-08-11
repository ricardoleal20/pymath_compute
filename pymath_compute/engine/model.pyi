"""
Rust models. Needed for all the important mathematical calculations
and mathematical operations
"""
from typing import TypeVar, Optional

Bound = TypeVar("Bound", int, float)


class EngineVar:
    """Rust Variable for the engine operations."""

    def __init__(
        self,
        name: str,
        lb: Bound = float("-inf"),
        ub: Bound = float("inf"),
        v0: Optional[Bound] = None,
        only_integer: bool = False
    ) -> None: ...
