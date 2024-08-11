"""
Optimization Solver Module

This module provides the `OptSolver` class for solving optimization problems.
The solver can be configured with variables, solver configuration, and an
objective function. It supports solving the problem and retrieving the results.

Classes:
    - OptSolver: Class for solving optimization problems.
    - OptSolverConfig: Configuration for the solver method
"""
import asyncio
import time
from functools import partial
from typing import (
    Literal, Callable, TypedDict,
    Awaitable, Any, Union,
    overload
)
# Local imports
from pymath_compute.methods import OptMethods
from pymath_compute.model.variable import Variable, MathExpression, MathFunction
from pymath_compute.utils.math_utils import get_max_int
# Import the rust constraint
from pymath_compute.engine.model import Constraint  # type: ignore

STATUS = Literal["OPTIMAL", "FEASIBLE", "UNFEASIBLE", "NOT_EXECUTED"]
MAX_INT = get_max_int()


class _Config(TypedDict):
    """Internal configuration for the solver"""
    solver_time: int
    solver_method: OptMethods


class OptSolverConfig(_Config, total=False):
    """Solver input configuration dictionary, that allow the user
    to implement easily the configuration for the solver Config
    """
    solver_time: int
    solver_method: OptMethods
    finite_var_step: float
    iterations: int
    tol: float
    learning_rate: float


class OptSolver:
    """
    Class OptSolver for solving optimization problems.
    
    Attributes:
        - status: Status of the solver.

    Methods:
        set_variables: Sets the variables to be considered in the algorithm.
        set_solver_config: Sets the solver configuration.
        set_objective_function: Sets the objective function.
        solve: Solves the optimization problem.
        vars_results: Returns the solution variables from the optimization.
    """
    _vars: list[Variable]
    _constraints: list[Constraint]
    _config: _Config
    _objective: Callable[[dict[str, int | float]], int | float]
    _results: list[Variable]
    _status: STATUS
    # Define the slots
    __slots__ = [
        "_vars",
        "_constraints",
        "_config",
        "_objective",
        "_results",
        "_status"
    ]

    def __init__(self) -> None:
        # Init the parameters
        self._status = "NOT_EXECUTED"
        self._vars = []
        self._constraints = []
        self._config = {  # type: ignore
            "solver_time": 30
        }
        self._objective = None  # type: ignore

    def __add_variable(self, **params) -> Variable:
        """Generic method to create variable"""
        var = Variable(**params)
        self._vars.append(var)
        return var

    def add_variable(self, name: str, lb: int | float, ub: int | float) -> Variable:
        """Create and add a variable to the model
        
        Args:
            - name: Unique identifier for the variable
            - lb: Lower bound of the variable
            - ub: Upper bound of the variable
        """
        return self.__add_variable(name=name, lb=lb, ub=ub)

    def add_int_variable(self, name: str, lb: int | float, ub: int | float) -> Variable:
        """Create and add an integer variable to the model
        
        Args:
            - name: Unique identifier for the variable
            - lb: Lower bound of the variable
            - ub: Upper bound of the variable
        """
        return self.__add_variable(name=name, lb=lb, ub=ub, only_integer=True)

    def add_bool_variable(self, name: str) -> Variable:
        """Create and add a boolean variable to the model
        
        Args:
            - name: Unique identifier for the variable
        """
        return self.__add_variable(name=name, lb=0, ub=1, only_integer=True)

    def add_constraint(
        self,
        expression: MathExpression | MathFunction,
        weight: int | float = 1
    ) -> Constraint:
        """Add a constraints for the solver. This constraint allow us
        to define limits on the solution
        
        Args:
            - Expression: Can be a MathExpression or a MathFunction
            - weight (optional[int]): Is the weight of the solution. This means
                how much it does care to the algorithm to minimize it or maximize it
        """
        constraint = Constraint(expression, weight)
        self._constraints.append(constraint)
        return constraint


    def set_variables(self, variables: list[Variable] | Variable) -> None:
        """Set Variables to be considered in the algorithm

        Args:
            - variables (List[Variable] | Variable) = Variables to be considered
                by the objective function of the algorithm
        """
        if isinstance(variables, list):
            if all(isinstance(v, Variable) is True for v in variables):
                self._vars += variables
            else:
                raise TypeError(
                    "In the given variables, at least one element is" +
                    " not type \"Variable\"."
                )
        elif isinstance(variables, Variable):
            self._vars.append(variables)
        else:
            raise TypeError(
                f"The type {type(variables)} is not implemented to set.")

    def set_solver_config(self, solver_config: OptSolverConfig) -> None:
        """Set different solver configuration.

        Between the solver configuration, you can found:
            - solver_time (int): Time in seconds that the solver has to find a solution.
                This time can be the maximum to search to the optimal solution.
            - solver_method (Methods): Enum of methods. You have to enter a valid input of
                the enum to tell the algorithm which method do you want to use.
                To use this, just import:
                    ```
                    from pymath_compute.methods import OptMethods
                    ```

        Args:
            - solver_config (OptSolverConfig): Include the configuration of the solver.
        """
        if not isinstance(solver_config, dict):
            raise TypeError("The configuration it should be a dictionary.")
        if not "solver_method" in solver_config:
            raise TypeError(
                "The solver configuration should incluye the Solver Method")
        if not isinstance(solver_config["solver_method"], OptMethods):
            raise TypeError(
                "The solver_config` is not an enum of type `OptMethods`. " +
                f"Instead is is of type {type(solver_config['solver_method'])}"
            )
        self._config.update(solver_config)

    @overload
    def set_objective_function(
        self,
        function: Callable[[dict[str, int | float]], int | float],
        **kwargs: Any
    ) -> None:
        ...

    @overload
    def set_objective_function(
        self,
        function: MathExpression | MathFunction
    ) -> None:
        ...

    def set_objective_function(
        self,
        function: Union[
            Callable[[dict[str, int | float]], int | float],
            Union[MathExpression, MathFunction]
        ],
        **kwargs: Any
    ) -> None:
        """Set the objective function. In can be a math expression or a math function
        or even a python function to calculate costs.

        This objective function should be of the form:
            ```
            def obj_func(vars: dict[str, int | float]) -> int | float:
                ...
            ```
        where the dictionary is going to be of type {var_name: var_value}

        Args:
            - function (Callable[[dict[str, int | float]]], int | float]): Function to calculate
                the objective functions to minimize.
        """
        if callable(function):
            self._objective = partial(function, **kwargs)
        elif isinstance(function, (MathFunction, MathExpression)):
            self._objective = function.evaluate
        else:
            raise NotImplementedError(
                "The function is not in the expected input parameters")

    def solve(self) -> None:
        """Solves the optimization problem.

        Raises:
            RuntimeError: If there are no variables to use, no
                objective function, or no solver method set.
        """
        if not self._vars:
            raise RuntimeError(
                "There are no variables to use in this solving method. " +
                "Please add them using `set_variables`."
            )
        if self._objective is None:
            raise RuntimeError(
                "There is no objective function to minimize. Please add it" +
                " using the method `set_objective_function`"
            )
        if self._config.get("solver_method", None) is None:
            raise RuntimeError("You haven't add the SolverMethod for this problem. Please" +
                               " add it using the `.set_solver_config` method")
        # Solve the problem
        self.__solve_problem()

    def vars_results(self) -> list[Variable]:
        """If the solver finds a solution, return the variables solution

        Returns:
            - Return the solution from the optimization
        """
        return self._vars

    @property
    def status(self) -> STATUS:
        """Status of the solver. This would tell us the final status
        of the problem, if it has find a solution, if it has not, or if it has
        not even been executed
        """
        return self._status

    # ==================================== #
    #            PRIVATE METHODS           #
    # ==================================== #
    def __solve_problem(self) -> None:
        """Solve the problem with the given results"""
        # Get the initial time of exec
        start_time = time.time()
        # Get the status
        try:
            self._status = asyncio.run(
                self.__execute_with_timeout_async(
                    self._config["solver_method"].value,
                    self._config["solver_time"]
                )
            )
        except TimeoutError:
            self._status = "FEASIBLE"
        except Exception as e:  # pylint: disable=W0718
            print("Error executing the algorithm:", e)
            self._status = "UNFEASIBLE"
        print(
            f"Solver ending with status {self._status}" +
            f" in {round(time.time() - start_time, 3)}s."
        )

    # ========================================== #
    #               Async executer               #
    # ========================================== #
    async def __execute_with_timeout_async(
        self,
        function: Callable[..., Awaitable[STATUS]],
        timeout: float
    ) -> STATUS:
        """Execute the optimization function using a timeout"""
        # Define their inputs
        inputs = {
            "variables": self._vars,
            "objective": self._objective,
            "constraints": self._constraints
        }
        for key, config in self._config.items():
            if key not in ["solver_method", "solver_time"]:
                inputs[key] = config
        try:
            return await asyncio.wait_for(
                function(**inputs),
                timeout
            )
        except asyncio.TimeoutError:
            raise TimeoutError(  # pylint: disable=W0707
                "Function execution timed out")
        except Exception as e:
            raise e
