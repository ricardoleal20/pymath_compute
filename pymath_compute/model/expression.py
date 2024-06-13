"""
MathExpression implementation module.

This module provides the implementation of the `MathExpression` class, which allows
the creation and manipulation of mathematical expressions involving variables, constants,
and functions. The expressions can be evaluated given a set of variable values.
"""
# Local import
from model.types import PosibleOperators, MathematicalTerms


class MathExpression:
    """Represents a mathematical expression, that can be a sum of two variables,
    a multiplication, a subtraction and other expressions.

    Attributes:
        terms (MathematicalTerms): The terms of the mathematical expression.
    """
    terms: MathematicalTerms
    __slots__ = ["terms"]

    def __init__(self, terms: MathematicalTerms) -> None:
        self.terms = terms

    def evaluate(self, values: dict[str, int | float]) -> float:
        """From a passed dictionary of values, we'll evaluate the current terms
        expression with that value.

        Example:
            ```
            x = Variable(name="x", lower_bound: 0, upper_bound: 10)
            expr = x + 2
            expr.evaluate({"x": 1}) <- We're setting the value for the name variable defined
            ```

        Args:
            values: dict[str, int | float]: A dict of values using the variable name as key
                and the value to set as the corresponding item for that key
        """
        if not isinstance(values, dict):
            raise TypeError("We're expecting a dict as {VAR_NAME: MATH_VALUE}," +
                            f" but instead we got {type(values)}.")
        # Initialize the result variable
        result: float = 0.0
        for var, coef in self.terms.items():
            # If the var is a constant, don't do
            # anything but adding them to the result
            if var == "const":
                result += coef
            elif type(var).__name__ == "Variable":
                if var.name not in values:
                    raise ValueError(
                        "In the given values, we're missing the" +
                        f" following variable '{var.name}'."
                    )
                result += coef*values[var.name]
            elif type(var).__name__ == "MathFunction":
                result += coef * var.evaluate(values)
            else:
                # Define a sub term for this
                sub_term = 1
                for v in var:
                    sub_term *= values[v.name]
                # In this situation, multiply the coef for the appended value
                result += coef * sub_term
        # In the end, return the result
        return result

    def __repr__(self) -> str:
        expression: str = "Expression: "
        # Add the terms to print in the representation
        printable_terms: list[str] = []
        for var, coef in self.terms.items():
            if var == "const":
                printable_terms.append(str(coef))
            elif type(var).__name__ == "Variable":
                printable_terms.append(f"{coef}*{var.name}")
            elif type(var).__name__ == "MathFunction":
                printable_terms.append(f"{coef}*{var}")
            else:
                # Define the str of the term
                # type: ignore
                term_str = '*'.join(v.name for v in var if not isinstance(v, str))
                # Define the printable terms here
                printable_terms.append(f"{coef}*{term_str}")
        # Return the expression with a join
        return expression + " + ".join(printable_terms)

    # ============================================= #
    #      MATH OPERATIONS REPLACING SECTION        #
    # ============================================= #

    # ////////////////////////// #
    #         ADD METHODS        #
    # ////////////////////////// #
    def __add__(self, other: PosibleOperators) -> 'MathExpression':  # pylint: disable=W0612
        # Obtain the new terms
        new_terms = self.terms.copy()
        if type(other).__name__ == "Variable":
            if other in new_terms:
                new_terms[other] += 1
            else:
                new_terms[other] = 1
        elif isinstance(other, MathExpression):
            for var, coef in other.terms.items():
                if var in new_terms:
                    new_terms[var] += coef
                else:
                    new_terms[var] = coef
        elif type(other).__name__ == "MathFunction":
            if other in new_terms:
                new_terms[other] += 1
            else:
                new_terms[other] = 1
        elif isinstance(other, (int, float)):
            if 'const' in new_terms:
                new_terms['const'] += other
            else:
                new_terms['const'] = other
        # Return the new MathExpression
        return MathExpression(new_terms)

    def __radd__(self, other: PosibleOperators) -> 'MathExpression':
        return self.__add__(other)

    # ////////////////////////// #
    #   MULTIPLICATION METHODS   #
    # ////////////////////////// #

    def __mul__(self, other: PosibleOperators) -> 'MathExpression':
        # Evaluate if the thing to evaluate is a int or a float
        if isinstance(other, (int, float)):
            # Get a new terms expression by multiplying everything that we have
            # for the new other term
            new_terms = {
                var: coef * other
                for var, coef in self.terms.items()
            }
            return MathExpression(new_terms)  # type: ignore
        if type(other).__name__ == "Variable":
            new_terms = {}
            for term, coef in self.terms.items():
                if isinstance(term, tuple):
                    new_terms[term + (other,)] = coef  # type: ignore
                else:
                    new_terms[(term, other)] = coef
            return MathExpression(new_terms)
        if type(other).__name__ == "MathFunction":
            new_terms = self.terms.copy()
            if other in new_terms:
                new_terms[other] += 1
            else:
                new_terms[other] = 1
            return MathExpression(new_terms)
        # If not, raise an error
        raise ValueError(
            "The MathExpression only allow us to add " +
            "integers, floats or another Variable."
        )

    def __rmul__(self, other: PosibleOperators) -> 'MathExpression':
        return self.__mul__(other)

    # ////////////////////////// #
    #     SUBTRACT METHODS       #
    # ////////////////////////// #

    def __sub__(self, other: PosibleOperators) -> 'MathExpression':
        return self.__add__(-other)  # type: ignore

    def __rsub__(self, other: PosibleOperators) -> 'MathExpression':
        # The (-self) invoques the __neg__ method and returns which value
        # we'll expect from it. Since we define the __neg__ method here, we already
        # know that we're going to get a new MathExpression with the negative values.
        return (-self).__add__(other)

    # ////////////////////////// #
    #      NEGATIVE METHODS      #
    # ////////////////////////// #

    def __neg__(self) -> 'MathExpression':
        # Obtain the new negative terms
        new_terms = {var: -coef for var, coef in self.terms.items()}
        return MathExpression(new_terms)
