"""..."""
from time import time
from typing import Callable, TypedDict
# Local imports
from pymath_compute.methods import Methods
from pymath_compute.model.variable import Variable


class SolverConfig(TypedDict):
    """Solver configuration dictionary"""
    solver_time: int
    solver_method: Methods


class Solver:
    """..."""
    _vars: list[Variable]
    _config: SolverConfig
    _objective: Callable[[list[Variable]], int | float]
    _results: list[Variable]
    _status: str
    # Define the slots
    __slots__ = [
        "_vars",
        "_config",
        "_objective",
        "_results",
        "_status"
    ]

    def __init__(self) -> None:
        # Init the parameters
        self._status = "NOT_EXECUTED"
        self._vars = []
        self._config = {  # type: ignore
            "solver_time": 30
        }
        self._objective = None  # type: ignore
        self._results = []

    def set_variables(self, variables: list[Variable] | Variable) -> None:
        """Set Variables to be considered in the algorithm
        
        Args:
            - variables (List[Variable] | Variable) = Variables to be considered
                by the objective function of the algorithm 
        """
        if isinstance(variables, list):
            self._vars += variables
        elif isinstance(variables, Variable):
            self._vars.append(variables)
        else:
            raise NotImplementedError(
                f"The type {type(variables)} is not implemented to set.")

    def set_solver_config(self, solver_config: SolverConfig) -> None:
        """Set different solver configuration.
        
        Between the solver configuration, you can found:
            - solver_time (int): Time in seconds that the solver has to find a solution.
                This time can be the maximum to search to the optimal solution.
            - solver_method (Methods): Enum of methods. You have to enter a valid input of
                the enum to tell the algorithm which method do you want to use.

        Args:
            - solver_config (SolverConfig): Include the configuration of the solver.
        """
        self._config.update(solver_config)

    def set_objective_function(self, function: Callable[[list[Variable]], int | float]) -> None:
        """Set the objective function.
        
        This objective function should be of the form:
            ```
            def obj_func(vars: list[Variable]) -> int | float:
                ...
            ```

        Args:
            - function (Callable[[list[Variable]], int | float]): Function to calculate
                the objective functions to minimize.
        """
        self._objective = function

    def solve(self) -> None:
        """..."""
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
        # Solve the problem
        self.__solve_problem()

    def vars_results(self) -> list[Variable]:
        """If the solver finds a solution, return the variables solution
        
        Returns:
            - Return the solution from the optimization
        """
        return self._results

    @property
    def status(self) -> str:
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
        # Store the time at which we initialize the solver
        start_execution: float = time()
        # Get the exec time
        exec_time = time() - start_execution
        if exec_time >= self._config["solver_time"]:
            self._status: str = "FEASIBLE"
        else:
            self._status: str = "OPTIMAL"
        print(
            f"Solver ending with status {self._status}" +
            f" in {exec_time}s."
        )
