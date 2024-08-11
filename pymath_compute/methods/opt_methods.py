"""
Optimization methods for the solvers
"""
from typing import Callable, Literal, TYPE_CHECKING
from enum import Enum
from functools import partial
# Local imports
from pymath_compute.model import Variable
from pymath_compute.engine.optimization_methods import (  # type: ignore
    gradient_descent, held_karp, brute_force  # type: ignore
)

if TYPE_CHECKING:
    from pymath_compute.solvers.opt_solver import Constraint  # type: ignore

STATUS = Literal["OPTIMAL", "FEASIBLE", "UNFEASIBLE", "NOT_EXECUTED"]


async def _gradient_descent(  # pylint: disable=R0913
    variables: list[Variable],
    constraints: list["Constraint"],
    objective: Callable[[dict[str, float]], float],
    *,
    finite_var_step: float = 0.001,
    learning_rate: float = 0.001,
    iterations: int = 1000,
    tol: float = 1e-6,
) -> STATUS:
    """Gradient Descent implementation

    This is a normal gradient descent implementation for a Python code.
    The values of the variables are updated in each iteration of the
    method, only if the old cost is better than the new cost.

    Args:
        - variables (list[Variable]): Variables given by the PyMath Module
        - objective (Callable): Method to calculate the cost.
        - var_step (float): Finite step to calculate the gradient
        - learning_rate (float): The learning rate for the variables
        - iterations (int): How many iterations are you going to run as max
        - tol (float): The tolerance to know if you got an optimal

    Returns:
        - The status of the method
    """
    if len(variables) < 2:
        raise RuntimeError(
            "This gradient method only works for more than 1 variable." +
            "Try making your solution space more finite."
        )
    if constraints:
        raise NotImplementedError(
            "The `Gradient Descent` method doesn't have compatibility with constraints.")
    # Just call the gradient descent method from the engine
    return gradient_descent(
        variables,
        objective,
        finite_var_step,
        learning_rate,
        iterations,
        tol
    )


async def _held_karp(
    variables: list[Variable],
    constraints: list["Constraint"],
    objective: Variable,
) -> STATUS:
    """Implementation of the Rust method Held Karp"""
    return held_karp(variables, constraints, objective)


async def _brute_force(
    variables: list[Variable],
    constraints: list["Constraint"],
    objective: Variable,
) -> STATUS:
    """Implementation of the Rust method Brute Force"""
    return brute_force(variables, constraints, objective)

# ===================== #
# Define the ENUM class #
# ===================== #


class OptMethods(Enum):
    """Available methods to use in the Solver
    
    Available methods are:
        * GRADIENT_DESCENT
        * HELD_KARP
        * BRUTE_FORCE
    """
    GRADIENT_DESCENT = partial(_gradient_descent)
    HELD_KARP = partial(_held_karp)
    BRUTE_FORCE = partial(_brute_force)
