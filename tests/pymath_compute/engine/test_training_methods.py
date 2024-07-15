"""
Implement tests for the solver engine.

In this case, we're going to solve the following problem:

```
    f(x) = e^{-x^2}; [-1, 1]
```
We'll calculate the minimum area of the curve in this function.

For the Area, we have:

```
    A = 2*pi*int( f(x) * sqrt(1 + (f'(x))^2 ) dx )
```
"""
from typing import Callable
import math
from functools import partial
import random
# External imports
import numpy as np
# Local imports
from pymath_compute.methods import Methods
from pymath_compute.solver import Solver
from pymath_compute import Variable, MathFunction, MathExpression


def _integrate(
    variable: Variable,
    math_expression: MathExpression
) -> float:
    """Integrate an expression using the MonteCarlo method"""
    # Discretize the space of the variable
    num_of_iterations: int = 100000
    # get the integral values
    # Get the limits from the variable
    lb = variable.lower_bound
    ub = variable.upper_bound
    # Get the random values
    random_int_value: float = 0.0
    for _ in range(num_of_iterations):
        # Evaluate the expression using a random value
        # for x
        random_int_value += math_expression.evaluate({
            variable.name: random.uniform(lb, ub)
        })
    # At the end, return the value
    return ((ub - lb)) / num_of_iterations * random_int_value


def cost(
    variables: list[Variable],
    expr: MathExpression
) -> int | float:
    """Cost function.
    This cost function is the
    """
    # For this, we'll divide the cost into three sections
    # SECTION 1 (section_one)
    # |-- 2 * pi
    section_one = 2*math.pi
    # SECTION 2 (section_two)
    # |-- integral ( expr * sqrt(1 + (derivate of expr)^2 ) dx )
    section_two = _integrate(
        variables[0],
        expr * MathFunction(
            math.sqrt,
            (1 + (2 * expr * variables[0]) ** 2)
        ).to_expression()
    )
    # section_two = expr * MathFunction(
    #     math.sqrt, 1+4 * variables[0] ** 2 *
    #     MathFunction(math.exp, -2 * variables[0] ** 2).to_expression()
    # ).to_expression()
    # At the end, we'll use to calculate the area
    # A = section_one * section_two
    return section_one * section_two


def init_solver(
    variables: list[Variable],
    cost_method: Callable[[list[Variable]], int | float]
) -> Solver:
    """Initialize the OPT Solver
    to use in this tests
    """
    solver = Solver()
    solver.set_variables(variables=variables)
    solver.set_objective_function(cost_method)
    # Set the parameters
    solver.set_solver_config({
        "solver_time": 30,
        "solver_method": Methods.GRADIENT_DESCENT
    })
    # Return the solver at the end
    return solver


def test_run_problem() -> None:
    """Test the problem spotted here beyond."""
    x = Variable("x", lb=-1, ub=1)
    # Define the expression
    expr = MathFunction(math.exp, (-x) ** 2).to_expression()
    # With this, define the cost method
    cost_method = partial(
        cost,
        integral=_integrate(
            x,
            expr * MathFunction(math.sqrt,
                                (1 + (2 * expr * x) ** 2)).to_expression()
        )
    )
    # Init the solver
    solver = init_solver([x], cost_method)
    # Run the solver
    solver.solve()
    # Get the results
    results = solver.vars_results()
    for result in results:
        print(result.value)
