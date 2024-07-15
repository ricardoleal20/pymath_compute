"""
Variable implementation. This method would allow us
to define and create a variable with a specific range [low_bound, upper_bound]

This variable would have a MathExpression instead of the normal
mathematical operations.
"""
from typing import Optional
# Local imports
from pymath_compute.model.types import Operators, Bound
from pymath_compute.model.expression import MathExpression


class Variable:
    """Represents a variable with a specific range [lower_bound, upper_bound].

    Attributes:
        name (str): The name of the variable.
        lb (int | float): The lower bound of the variable's range.
            Default to -infinite
        ub (int | float): The upper bound of the variable's range.
            Default to infinite
    """
    _name: str
    lower_bound: float
    upper_bound: float
    _value: Optional[float]
    # Define the slots to save memory space
    __slots__ = ["_name", "lower_bound", "upper_bound", "_value"]

    def __init__(
        self,
        name: str,
        lb: Bound = float("-inf"),
        ub: Bound = float("inf")
    ) -> None:
        # Evaluate that the parameters are correct
        if not isinstance(name, str):
            raise TypeError("The name should be a string, but instead" +
                            f" is {type(name)}.")
        if not isinstance(lb, (int, float)) or not isinstance(ub, (int, float)):
            raise TypeError(
                "The lower bound and the upper bound should be" +
                " floats, but instead they are: " +
                f"LB={type(lb)} | UP={type(ub)}."
            )
        if lb > ub:
            raise ValueError("The lower bound should be lower than the upper bound" +
                             f" but we have LB={lb} > UP={ub}.")
        # If everything is okay, set the values
        self._name = name
        self.lower_bound = lb
        self.upper_bound = ub
        self._value = None

    @property
    def name(self) -> str:
        """Variable name. This is an unique identifier to found them and use
        their value in different positions
        
        Returns:
            str: The variable name
        """
        return self._name

    @property
    def value(self) -> float:
        """Get the current value of the variable used for mathematical operations.
        
        Returns:
            float: The current value of the variable.
        """
        return self._value if self._value else 0.0

    @value.setter
    def value(self, new_value: float) -> None:
        """Set a new value for this variable:

        Args:
            - new_value (float): New value to set

        Raises:
            ValueError: If the value set is not in the defined
                    [lower_bound, upper_bound] range.
        """
        # Evaluate if the value is inside the range
        if self.lower_bound <= new_value <= self.upper_bound:
            self._value = new_value
            return
        # If not, raise an error
        raise ValueError(
            f"The new expected value {new_value} is outside the range of" +
            f" [{self.lower_bound}, {self.upper_bound}]."
        )

    def to_expression(self) -> 'MathExpression':
        """Convert this Variable into a MathExpression"""
        return MathExpression({self: 1})

    def plot(self) -> None:
        """Plot this variable with their corresponding limits"""
        self.to_expression().plot()

    def __repr__(self) -> str:
        if self._value is not None:
            return f"{self.name}: {self._value}"
        return self.name

    # ============================================= #
    #      MATH OPERATIONS REPLACING SECTION        #
    # ============================================= #

    # ////////////////////////// #
    #         ADD METHODS        #
    # ////////////////////////// #
    def __add__(self, other: Operators) -> 'MathExpression':
        # Evaluate if the other param is a Variable
        if isinstance(other, Variable):
            return MathExpression({self: 1, other: 1})
        if isinstance(other, MathExpression):
            return other + self
        if type(other).__name__ == "MathFunction":
            return MathExpression({self: 1, other: 1})
        if isinstance(other, (int, float)):
            return MathExpression({self: 1, 'const': other})
        # If there's no one of this parameters, raise an error
        raise TypeError(
            f"Cannot append {other} of type {type(other)} as a expression."
        )

    def __radd__(self, other: Operators) -> 'MathExpression':
        return self.__add__(other)

    # ////////////////////////// #
    #   MULTIPLICATION METHODS   #
    # ////////////////////////// #

    def __mul__(self, other: Operators) -> 'MathExpression':
        if isinstance(other, Variable):
            return MathExpression({(self, other): 1})
        if type(other).__name__ == "MathFunction":
            return MathExpression({self: 1, other: 1})
        if isinstance(other, (int, float)):
            return MathExpression({self: other})
        # If there's no one of this parameters, raise an error
        raise TypeError(
            f"Cannot append {other} of type {type(other)} as a expression."
        )

    def __rmul__(self, other: Operators) -> 'MathExpression':
        return self.__mul__(other)

    # ////////////////////////// #
    #     SUBTRACT METHODS       #
    # ////////////////////////// #

    def __sub__(self, other: Operators) -> 'MathExpression':
        return self.__add__(other)

    def __rsub__(self, other: Operators) -> 'MathExpression':
        return -self.__sub__(other)

    # ////////////////////////// #
    #      NEGATIVE METHODS      #
    # ////////////////////////// #

    def __neg__(self) -> 'MathExpression':
        return MathExpression({self: -1})

    # ////////////////////////// #
    #    EXPONENTIAL METHODS     #
    # ////////////////////////// #

    def __pow__(self, power_value: int) -> 'MathExpression':
        if isinstance(power_value, int) and power_value >= 0:
            return MathExpression({(self,)*power_value: 1})  # type: ignore
        raise TypeError(
            "For the moment, the only power values " +
            "that we have implemented are: [int]."
        )
