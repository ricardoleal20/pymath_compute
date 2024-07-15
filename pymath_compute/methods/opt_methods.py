"""
Optimization methods for the solvers
"""
from typing import Callable, Literal
from enum import Enum
from functools import partial
# Local imports
from pymath_compute.model import Variable
from pymath_compute.engine.optimization_methods import gradient_descent

STATUS = Literal["OPTIMAL", "FEASIBLE", "UNFEASIBLE", "NOT_EXECUTED"]


async def _gradient_descent(  # pylint: disable=R0913
    variables: list[Variable],
    cost_method: Callable[[dict[str, float]], float],
    *,
    finite_var_step: float = 0.001,
    learning_rate: float = 0.001,
    iterations: int = 1000,
    tol: float = 1e-6,
) -> STATUS:
    """..."""
    # Just call the gradient descent method from the engine
    return gradient_descent(
        variables,
        cost_method,
        finite_var_step,
        learning_rate,
        iterations,
        tol
    )

# ===================== #
# Define the ENUM class #
# ===================== #


class OptMethods(Enum):
    """Available methods to use in the Solver
    
    Available methods are:
        * GRADIENT_DESCENT
    """
    GRADIENT_DESCENT = partial(_gradient_descent)
