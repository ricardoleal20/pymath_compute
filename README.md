# PyMathCompute

<img src="https://github.com/ricardoleal20/pymath_compute/blob/main/docs/public/logo.png" />

**PyMathCompute** is a Python tool designed to handle mathematical variables, create and evaluate mathematical expressions, and perform various mathematical optimizations. This library is ideal for those working in applied mathematics, optimization, and related fields.

## Features

- **Variable**: Defines mathematical variables with lower and upper bounds.
- **MathExpression**: Creates and evaluates mathematical expressions using defined variables.
- **Mathematical Operations**: Supports addition, subtraction, multiplication, and exponentiation of variables and expressions.

## Installation

You can install PyMathCompute using pip:

```bash
pip install pymath_compute
```

## Basic Usage

### Defining Variables and Mathematical Expressions

```python
from pymath_compute import Variable

# Create a variable
x = Variable(name="x", lower_bound=0, upper_bound=10)

# Create a mathematical expression
expr = x + 2 * x - 5

# Evaluate the expression
values = {"x": 5}
result = expr.evaluate(values)
print(f"Result of the expression: {result}")
```

### Mathematical Operations

PyMathCompute allows various mathematical operations with variables and expressions:

```python
from pymath_compute import Variable

# Create variables
x = Variable(name="x", lower_bound=0, upper_bound=10)
y = Variable(name="y", lower_bound=0, upper_bound=10)

# Create expressions
expr1 = x + y
expr2 = x * 2 + y ** 2

# Evaluate expressions
values = {"x": 3, "y": 4}
result1 = expr1.evaluate(values)
result2 = expr2.evaluate(values)

print(f"Result of expr1: {result1}")
print(f"Result of expr2: {result2}")
```

### Mathematical Operators

PyMathCompute also allow connection with operators, as using `sin`, `cos`, `e`, and others. For this, we use the `MathFunction` parameter

```python
from numpy import np
from pymath_compute import Variable, MathFunction

# Create the variables
x = Variable(name="x", lower_bound=0, upper_bound=np.pi)

# Add a function to calculate the sin of x
sin = MathFunction(np.sin, x)
```

## Future Plans

In future versions, we plan to add:

- Mathematical optimization methods like Newton's method.
- Molecular dynamics solvers.
- Computational derivatives and other advanced calculus tools.

## Contributions

Contributions are welcome. If you have suggestions, bug reports, or improvements to propose, please open an issue or a pull request on our GitHub repository.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/ricardoleal20/pymath_compute/blob/main/LICENSE) file for details.

---

We hope PyMathCompute is useful for your mathematical and optimization needs. Happy calculating!
