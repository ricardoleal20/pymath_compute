"""
MathFunction implementation module.

This module provides the implementation of the `MathFunction` class, which allows
the creation and manipulation of mathematical functions involving variables. The 
functions can be evaluated given a set of variable values.
"""
from typing import Callable, TypeVar, Union, Optional, TYPE_CHECKING
from pymath_compute.model.expression import MathExpression
if TYPE_CHECKING:
    from pymath_compute.model.variable import Variable

FunctionReturn = TypeVar("FunctionReturn", int, float)


class MathFunction:
    """Represents a mathematical function.

    Attributes:
        function (Callable[..., FunctionReturn]): The function to be evaluated.
        variable (Union[Variable, MathExpression]): The variable or expression
                involved in the function.

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
        variable: Union['Variable', MathExpression, "MathFunction"]
    ) -> None:
        self.function = function
        self.variable = variable

    def evaluate(self, values: Optional[dict] = None) -> float:
        """Evaluate the mathematical function using the provided variable values.
        If we do not provide any dictionary with values, we'll use the variable.value
        given

        Args:
            values (dict): A dictionary of values using the variable names as keys
                and the corresponding values to set for those variables.

        Returns:
            float: The result of the function evaluation.

        Raises:
            ValueError: If the required variable is not included in the provided values.
        """
        if values is None:
            values = {}
        if isinstance(self.variable, (MathExpression, MathFunction)):
            return self.function(self.variable.evaluate(values))
        if type(self.variable).__name__ == "Variable":
            # If the variable is on values
            if self.variable.name in values:
                return self.function(values[self.variable.name])
            if self.variable in values:
                return self.function(values[self.variable])

        return self.function(self.variable.value)

    def to_expression(self) -> 'MathExpression':
        """Convert this Function into a MathExpression"""
        return MathExpression({self: 1})

    def plot(self) -> None:
        """Plot this mathematical function with their corresponding limits"""
        self.to_expression().plot()

    def __repr__(self) -> str:
        return f"Function[{self.function.__name__}({self.variable})]"

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
        if type(other).__name__ in ("Variable", "MathExpression"):
            return MathExpression({self: 1, other: 1})

        raise ValueError("There's no implemented addition for this two types.")

    def __radd__(self, other):
        return self.__add__(other)

    # /////////////////////////// #
    #     COMPARISON METHODS      #
    # /////////////////////////// #

    def __eq__(self, other: Union["Variable", "MathFunction", float, int]) -> "MathFunction":
        """Overload the == operator"""
        from pymath_compute.utils.math_utils import get_max_int  # pylint: disable=C0415
        max_int = get_max_int()

        def equal_to(value: int | float) -> int:
            if type(other).__name__ == "Variable":
                return max_int*(1-int(value == other.value))  # type: ignore
            if isinstance(other, MathFunction):
                return max_int*(1-int(value == other.evaluate()))
            if isinstance(other, MathExpression):
                return max_int*(1-int(value == other.evaluate()))
            if isinstance(other, (float, int)):
                return max_int*(1-int(value == other))
            # If it is not, raise an error
            raise NotImplementedError(
                f"The equal to between {self} and {other}" +
                f" of type {type(other)} is not implemented"
            )
        return MathFunction(equal_to, self)

    # /////////////////////////// #
    #        HASH METHODS         #
    # /////////////////////////// #
    def __hash__(self) -> int:
        return hash((id(self), id(self.variable), id(self.function)))
