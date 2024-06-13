"""
Variable implementation. This method would allow us
to define and create a variable with a specific range [low_bound, upper_bound]

This variable would have a MathExpression instead of the normal
mathematical operations.
"""
from typing import Optional
# Local imports
from model.types import PosibleOperators
from model.expression import MathExpression


class Variable:
    """Represents a variable with a specific range [lower_bound, upper_bound].

    Attributes:
        name (str): The name of the variable.
        lower_bound (float): The lower bound of the variable's range.
        upper_bound (float): The upper bound of the variable's range.
    """
    name: str
    lower_bound: float
    upper_bound: float
    _value: Optional[float]
    # Define the slots to save memory space
    __slots__ = ["name", "lower_bound", "upper_bound", "_value"]

    def __init__(
        self,
        name: str,
        lower_bound: int | float,
        upper_bound: int | float
    ) -> None:
        # Evaluate that the parameters are correct
        if not isinstance(name, str):
            raise TypeError("The name should be a string, but instead" +
                            f" is {type(name)}.")
        if not isinstance(lower_bound, (int, float)) or not isinstance(upper_bound, (int, float)):
            raise TypeError(
                "The lower bound and the upper bound should be" +
                " floats, but instead they are: " +
                f"LB={type(lower_bound)} | UP={type(upper_bound)}."
            )
        if lower_bound > upper_bound:
            raise ValueError("The lower bound should be lower than the upper bound" +
                             f" but we have LB={lower_bound}>UP={upper_bound}.")
        # If everything is okay, set the values
        self.name = name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self._value = None

    @property
    def value(self) -> float:
        """Get the current value of the variable used for mathematical operations.
        
        Returns:
            float: The current value of the variable.
        """
        return self._value

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

    def __repr__(self) -> str:
        if self.value is not None:
            return f"{self.name}: {self.value}"
        return self.name

    # ============================================= #
    #      MATH OPERATIONS REPLACING SECTION        #
    # ============================================= #

    # ////////////////////////// #
    #         ADD METHODS        #
    # ////////////////////////// #
    def __add__(self, other: PosibleOperators) -> 'MathExpression':
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

    def __radd__(self, other: PosibleOperators) -> 'MathExpression':
        return self.__add__(other)

    # ////////////////////////// #
    #   MULTIPLICATION METHODS   #
    # ////////////////////////// #

    def __mul__(self, other: PosibleOperators) -> 'MathExpression':
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

    def __rmul__(self, other: PosibleOperators) -> 'MathExpression':
        return self.__mul__(other)

    # ////////////////////////// #
    #     SUBTRACT METHODS       #
    # ////////////////////////// #

    def __sub__(self, other: PosibleOperators) -> 'MathExpression':
        return self.__add__(other)

    def __rsub__(self, other: PosibleOperators) -> 'MathExpression':
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
        raise NotImplementedError(
            "For the moment, the only power values " +
            "that we have implemented are: [int]."
        )
