/// Include several optimization techniques.
/// For this module, the techniques are of type `search`,
/// since we're searching.
///
use pyo3::prelude::*;
use pyo3::PyResult;
// Local imports
use crate::math_utilities::convert_to_ref;

#[pyfunction]
pub fn held_karp(variables: &PyAny) -> PyResult<&'static str> {
    // Provide the status
    let status = "UNKNOWN";
    // Get the mut variables
    let mut_vars = convert_to_ref(variables)?;
    // Get the number of elements
    let n_elements = mut_vars.len();
    // Return the status at the very end
    Ok(status)
}

#[pyfunction]
pub fn brute_force(variables: &PyAny) -> PyResult<&'static str> {
    // Provide the status
    let status = "UNKNOWN";
    // Get the mut variables
    let mut_vars = convert_to_ref(variables)?;
    // Get the number of elements
    let n_elements = mut_vars.len();
    // Return the status at the very end
    Ok(status)
}
