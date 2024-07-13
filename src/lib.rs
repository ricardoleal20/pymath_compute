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
fn engine(py: Python, m: &PyModule) -> PyResult<()> {
    // Call all the modules and append those modules to the main module //
    // MODULE METHODS.
    let optimization = build_optimization_module(py)?;
    // ================================================================= //
    // Add all the PyModules to the main m module                        //
    // ================================================================= //
    m.add_submodule(optimization)?;
    // Return the result of the module at the very end                   //
    Ok(())
}

/// Include several optimization methods to handle the optimization
/// of different functions
fn build_optimization_module(py: Python) -> Result<&PyModule, PyErr> {
    // Let's add a new submodule for the methods
    let methods_module = PyModule::new(py, "optimization_methods")?;
    // Add the methods inside here
    methods_module.add_function(wrap_pyfunction!(gradient_descent, methods_module)?)?;
    // Return the methods module
    Ok(methods_module)
}
