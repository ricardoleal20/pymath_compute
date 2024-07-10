//! Library export for Python modules
//!
// Import the methods module here
mod methods;
// Import/ use methods
use methods::training::*;
use pyo3::prelude::*;

/// Mathematical engine for all heavy mathematical computations
/// made it in Rust. This engine allow us to implement and use
/// different functions or optimization methods in Python code,
/// allowing us to have an increase in the execution time and
/// in the convergence.
///  
/// The modules now includes in this engine are:
///     - methods: Include different set of methods
#[pymodule]
fn pymath_compute_engine(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(gradient_descent, m)?)?;
    Ok(())
}
