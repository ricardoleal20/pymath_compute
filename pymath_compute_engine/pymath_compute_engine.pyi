"""
Mathematical engine for all heavy mathematical computations
made it in Rust. This engine allow us to implement and use
different functions or optimization methods in Python code,
allowing us to have an increase in the execution time and
in the convergence.
 
The modules now includes in this engine are:
    - methods: Include different set of methods
"""


def gradient_descent(
    x: float,
    learning_rate: float,
    iterations: int
) -> float:
    """Perform gradient descent optimization.
    Arguments:
        - `x`: The initial value.
        - `learning_rate`: The step size for each iteration.
        - `iterations`: The number of iterations to perform.
        - `grad`: The gradient function.

    Returns:
        The optimized value after performing gradient descent.
    """
