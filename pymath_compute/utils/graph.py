"""
Implement a generic code that allows us to graph a mathematical expression and a given value.

This module provides functions to obtain variables from a mathematical expression and to plot 
a mathematical expression with specified limits for the variables.

Classes:
    VarsLimit: Represents the upper and lower limits to plot an expression.

Functions:
    plot_math_expression:
        Plots a mathematical expression with specified limits for the variables and optional 
        parameters for customization.
"""
from typing import TypedDict, Optional, TYPE_CHECKING
import random
# Required Math imports
import numpy as np
import matplotlib.pyplot as plt
# Local imports
if TYPE_CHECKING:
    from pymath_compute.model.expression import MathExpression
    from pymath_compute.model.variable import Variable

# Add this to allow us to import everything in a LaTex manner
font = {
    'family': 'serif',
    'size': 12,
    'serif':  'Computer Modern'
}


class VarsLimit(TypedDict):
    """Upper and Lower limit to plot an expression"""
    lower_limit: Optional[float]
    upper_limit: Optional[float]


def _get_vars(expression: "MathExpression") -> set["Variable"]:
    """
    Retrieves all variables involved in a mathematical expression.

    Args:
        expression (MathExpression): The mathematical expression from which to extract variables.

    Returns:
        set[Variable]: A set of variables involved in the expression.
    """
    variables: set["Variable"] = set()
    for term in expression.terms.keys():
        if not isinstance(term, tuple):
            term = (term, )  # type: ignore
        for t in term:  # type: ignore
            if type(t).__name__ == "Variable":
                variables.add(t)  # type: ignore
            if type(t).__name__ == "MathFunction":
                if type(t.variable).__name__ == "Variable":  # type: ignore
                    variables.add(t.variable)  # type: ignore
                else:
                    variables = variables | _get_vars(
                        t.variable)  # type: ignore
    # Return the variables obtained
    return variables


def plot_math_expression(  # pylint: disable=R0913
    expr: "MathExpression",
    *,
    store_as_pdf: bool = False,
    vars_limit: Optional[dict["Variable", VarsLimit]] = None,
    figsize: tuple[int, int] = (10, 6),
    xlabel: str = "Variable values",
    ylabel: str = "Expression values"
) -> None:
    """Plots a mathematical expression with specified limits for
    the variables and optional parameters for customization.

    Args:
        expr (MathExpression): The mathematical expression to plot.
        store_as_pdf (bool, optional): Whether to store the plot as a PDF file. Defaults to False.
        vars_limit (Optional[dict[Variable, VarsLimit]], optional): A dictionary specifying the
            limits for each variable. Defaults to None.
        figsize (tuple[int, int], optional): The size of the figure. Defaults to (10, 6).
        xlabel (str, optional): The label for the x-axis. Defaults to "Variable values".
        ylabel (str, optional): The label for the y-axis. Defaults to "Expression values".
    """
    # From the expression, get the terms inside it
    variables: set["Variable"] = set(  # type: ignore
        var for var in expr.terms.keys()
        if type(var).__name__ == "Variable"
    )

    variables: set["Variable"] = _get_vars(expression=expr)
    vars_limit = vars_limit if vars_limit else {}
    # From each of the variable, get a linspace
    for var in variables:
        if var in vars_limit:
            if "lower_limit" not in vars_limit[var]:
                vars_limit[var]["lower_limit"] = var.lower_bound
            if "upper_limit" not in vars_limit[var]:
                vars_limit[var]["upper_limit"] = var.upper_bound
        else:
            vars_limit[var] = {
                "lower_limit": var.lower_bound,
                "upper_limit": var.upper_bound
            }
    # With this limits, get the values per each variable
    values_per_variable = {
        var.name: np.linspace(
            limits["lower_limit"],  # type: ignore
            limits["upper_limit"]  # type: ignore
        )
        for var, limits in vars_limit.items() if limits
    }
    # And get the general expression value
    expr_values: list[float] = []
    for values in zip(*values_per_variable.values()):
        # Get the values to evaluate in this iteration and evaluate the expression
        # for this items
        expr_values.append(
            expr.evaluate(
                dict(zip(values_per_variable.keys(), values))  # type: ignore
            )
        )
    # Then, start to plot the figure
    plt.figure(figsize=figsize)
    # Add the lines
    colors = ["black", "red", "gold", "blue", "green"]
    random.shuffle(colors)
    i: int = 0
    for variable, values in values_per_variable.items():
        i += 1
        plt.plot(values, expr_values, label=variable, color=colors[i])
    # Add the labels
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f'Graph of ${expr}$.')
    plt.legend()
    # Show grid
    plt.grid(True)
    # Decide if you want to store this graph or to show it
    if store_as_pdf is False:
        plt.show()
    else:
        plt.savefig(f'{expr}.pdf', format='pdf')
