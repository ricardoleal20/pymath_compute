"""
Get types to use in common around the model definition
"""
from typing import TypeVar, Union, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from pymath_compute.model.variable import Variable
    from pymath_compute.model.expression import MathExpression

Operators = TypeVar(
    "Operators",
    # Math the operators
    'Variable',  'MathExpression',  int, float
)
Term = TypeVar("Term", str, "Variable")

MathematicalTerms = Dict[Term, float]

# Define the bound
Bound = TypeVar("Bound", int, float)
