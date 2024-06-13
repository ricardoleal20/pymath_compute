"""
Get types to use in common around the model definition
"""
from typing import Union, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from model.variable import Variable
    from model.expression import MathExpression

PosibleOperators = Union['Variable',  'MathExpression',  int, float]
MathematicalTerms = Dict[Union['Variable', str], float]
