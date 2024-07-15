"""
Mathematical engine for all heavy mathematical computations
made it in Rust. This engine allow us to implement and use
different functions or optimization methods in Python code,
allowing us to have an increase in the execution time and
in the convergence.
 
The modules now includes in this engine are:
    - methods: Include different set of methods
"""
from typing import Callable, Literal
# Local imports
from pymath_compute.model import Variable

STATUS = Literal["OPTIMAL", "FEASIBLE", "UNFEASIBLE", "NOT_EXECUTED"]


def gradient_descent(
    variables: list[Variable],
    cost_method: Callable[[dict[str, float]], float | int],
    var_step: float,
    learning_rate: float,
    iterations: int,
    tol: float,
) -> STATUS:
    """..."""
