"""
Methods to use to solve this computation methods.

In here, you can an enum of the methods that you can use
"""
from enum import Enum
# Make also local imports
from pymath_compute.methods.training import gradient_descent


class Methods(Enum):
    """Available methods to use in the Solver
    
    Available methods are:
        - Interpolation:
            ...
        - Regularity:
            ...
        - Search:
            ...
        - Training:
            * GRADIENT_DESCENT
    """
    GRADIENT_DESCENT = gradient_descent
