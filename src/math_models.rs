/// PYTHON MODELS
///
/// Define some references for the python models such as:
///     - Variable
///     - MathFunction
///     - MathExpression
///
/// This allow us to interact with them in Rust, giving us the change
/// to get their values, set new values and things similar to that
use pyo3::prelude::*;

// ==================================== //
//              VARIABLE                //
// ==================================== //
/// Rust interpreter for the Variable class of the
/// Python module of PyMath Compute
#[pyclass]
pub struct Variable {
    pub name: String,
    value: f64,
}

#[pymethods]
impl Variable {
    #[new]
    fn new(name: String, value: f64) -> Self {
        Variable { name, value }
    }

    #[getter]
    pub fn get_name(&self) -> &str {
        &self.name
    }

    #[getter]
    pub fn get_value(&self) -> f64 {
        self.value
    }

    #[setter]
    pub fn set_value(&mut self, value: f64) {
        self.value = value;
    }
}
