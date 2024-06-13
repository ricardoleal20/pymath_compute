"""
MathFunction implementation module.

This module provides the implementation of the `MathFunction` class, which allows
the creation and manipulation of mathematical functions involving variables. The 
functions can be evaluated given a set of variable values.
"""
from typing import Callable, TypeVar, TYPE_CHECKING
from model.expression import MathExpression
if TYPE_CHECKING:
    from model.variable import Variable

FunctionReturn = TypeVar("FunctionReturn", int, float)


class MathFunction:
    """Represents a mathematical function.

    Attributes:
        function (Callable[..., FunctionReturn]): The function to be evaluated.
        variable (Variable): The variable involved in the function.

    Example:
        ```
        import numpy as np
        from pymath_compute import Variable, MathFunction

        # Create the variable 
        x = Variable(name="X", lower_bound=0, upper_bound=10)
        # Create a sin expression
        sin = MathFunction(np.sin, x)
        ```
    """
    __slots__ = ["function", "variable"]

    def __init__(
        self,
        function: Callable[..., FunctionReturn],
        variable: 'Variable'
    ) -> None:
        self.function = function
        self.variable = variable

    def evaluate(self, values: dict) -> float:
        """Evaluate the mathematical function using the provided variable values.

        Args:
            values (dict): A dictionary of values using the variable names as keys
                and the corresponding values to set for those variables.

        Returns:
            float: The result of the function evaluation.

        Raises:
            ValueError: If the required variable is not included in the provided values.
        """
        if self.variable.name not in values:
            raise ValueError(
                f"The variable {
                    self.variable.name} is not in the given values."
            )
        return self.function(values[self.variable.name])

    def __repr__(self) -> str:
        return f"{self.function.__name__}({self.variable.name})"

    # ============================================= #
    #      MATH OPERATIONS REPLACING SECTION        #
    # ============================================= #

    # ////////////////////////// #
    #         ADD METHODS        #
    # ////////////////////////// #

    def __add__(self, other) -> MathExpression:
        if isinstance(other, MathFunction):
            return MathExpression({self: 1, other: 1})
        if isinstance(other, (int, float)):
            return MathExpression({self: 1, 'const': other})
        # Evaluate the name of the type
        var_type_name = type(other).__name__
        if var_type_name == "Variable" or var_type_name == "MathExpression":
            return MathExpression({self: 1, other: 1})

        raise ValueError("There's no implemented addition for this two types.")

    def __radd__(self, other):
        return self.__add__(other)
