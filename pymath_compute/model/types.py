"""
Get types to use in common around the model definition
"""
from typing import TypeVar, Union, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from pymath_compute.model.variable import Variable
    from pymath_compute.model.function import MathFunction
    from pymath_compute.model.expression import MathExpression

# ===================================== #
#               TypeVar                 #
# ===================================== #
Operators = TypeVar(
    "Operators",
    # Math the operators
    'Variable',  'MathExpression', int, float
)
Term = TypeVar("Term", str, "Variable")
# Define the bound
Bound = TypeVar("Bound", int, float)

# ===================================== #
#                Terms                  #
# ===================================== #
MathematicalTerms = Dict[
    Union[
        "Variable",
        "MathFunction",
        tuple["Variable", "Variable"],
        str
    ],
    float | int
] | Dict[
    Union["Variable", "MathExpression", int, float],
    int | float
]
