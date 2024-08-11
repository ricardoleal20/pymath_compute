/// Utilities without an specific function
///
use pyo3::prelude::*;
use pyo3::types::PyList;
// Local imports
use crate::model::EngineVar;

pub fn convert_to_ref(variables: &PyAny) -> Result<Vec<PyRefMut<EngineVar>>, PyErr> {
    // Convert the PyAny into a PyList
    let variables_list: &PyList = variables.downcast()?;

    // Create the vector to store this references
    let mut variable_refs: Vec<PyRefMut<EngineVar>> = Vec::new();

    // Iterate over the elements in the PyList
    for item in variables_list.iter() {
        // convert the item into a cell of type &PyCell<EngineVar>
        let py_cell: &PyCell<EngineVar> = item.downcast()?;

        // Finally, push and store the mutable reference
        variable_refs.push(py_cell.borrow_mut());
    }
    // Return the ref
    Ok(variable_refs)
}
