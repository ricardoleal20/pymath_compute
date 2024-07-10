//! Trainable methods for Optimization
//!
//! Provides different methods that include training, such as:
//!     - Gradient Descendent
//!
use pyo3::prelude::*;

/// Perform gradient descent optimization.
///
/// # Arguments
///
/// * `x` - The initial value.
/// * `learning_rate` - The step size for each iteration.
/// * `iterations` - The number of iterations to perform.
/// * `grad` - The gradient function.
///
/// # Returns
///
/// The optimized value after performing gradient descent.
#[pyfunction]
pub fn gradient_descent(x: f64, learning_rate: f64, iterations: usize) -> PyResult<f64> {
    let mut calc_x: f64 = x;
    // Iterate over the number of given iterations
    for _ in 0..iterations {
        // Calculate the new x
        calc_x -= learning_rate * 2.0 * x;
    }
    Ok(calc_x)
}
