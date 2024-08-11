use pyo3::prelude::*;
use pyo3::types::PyDict;

/// Constraint for the Optimization problem modeled
#[pyclass]
pub struct Constraint {
    _expression: PyObject,
    _weight: f64,
}

#[pymethods]
impl Constraint {
    #[new]
    fn new(expression: PyObject, weight: f64) -> Self {
        Constraint {
            _expression: expression,
            _weight: weight,
        }
    }

    fn __call__(&self, py: Python, values: Option<&PyDict>) -> PyResult<f64> {
        let const_val = self.value(py, values)?;
        if const_val == f64::INFINITY {
            Ok(f64::INFINITY)
        } else {
            Ok(const_val)
        }
    }

    /// Get the value of the constraint.
    ///    
    /// If you constraint is a hard constraint (meaning, that it's weight
    /// is infinite or that is a == expression, ...)
    fn value(&self, py: Python, values: Option<&PyDict>) -> PyResult<f64> {
        // Call the `evaluate` method of `_expression` passing the `values`
        let evaluate_func = self
            ._expression
            .call_method(py, "evaluate", (values,), None)?;
        let result: f64 = evaluate_func.extract(py)?;
        Ok(self._weight * result)
    }

    /// Evaluate if the math expression is validated
    fn is_satisfied(&self, py: Python, values: Option<&PyDict>) -> PyResult<i32> {
        let const_val = self.value(py, values)?;
        if const_val == f64::INFINITY {
            Ok(0)
        } else {
            Ok(1)
        }
    }

    // Add __repr__ method
    fn __repr__(&self, py: Python) -> PyResult<String> {
        let expr_repr = self._expression.call_method(py, "__repr__", (), None)?;
        let expr_str: String = expr_repr.extract(py)?;
        Ok(format!("CONSTRAINT::{}*{}", self._weight, expr_str))
    }
}
