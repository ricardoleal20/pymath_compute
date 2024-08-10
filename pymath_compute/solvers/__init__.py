"""
Include different solvers for different kinds of problems.
Each solver has an unique structure and an unique way to be implemented
allowing us to achieve different problems in different scenarios.

The available solvers are:

    - **OptSolver**: Solver for optimization problems, such as
        the Gradient Descent method
"""
from pymath_compute.solvers.opt_solver import OptSolver, OptSolverConfig, OptMethods

__all__ = [
    "OptSolver",
    "OptMethods",
    "OptSolverConfig"
]

__configs__ = [
    OptSolverConfig
]

__methods__ = {
    OptMethods
}
