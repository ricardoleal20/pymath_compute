/// Utilities without an specific function
///
use itertools::{Itertools, MultiProduct};
use pyo3::prelude::*;
use pyo3::types::PyList;
use std::collections::HashMap;
use std::vec::IntoIter;
// Local imports
use crate::model::{Constraint, EngineVar};

pub fn convert_to_var_ref(variables: &PyAny) -> Result<HashMap<&str, &PyCell<EngineVar>>, PyErr> {
    // Convert the PyAny into a PyList
    let variables_list: &PyList = variables.downcast()?;

    // Create the vector to store this references
    let mut variable_refs: HashMap<&str, &PyCell<EngineVar>> = HashMap::new();

    // Iterate over the elements in the PyList
    for item in variables_list.iter() {
        // convert the item into a cell of type &PyCell<EngineVar>
        let py_cell: &PyCell<EngineVar> = item.downcast()?;
        let var_name = py_cell.getattr("name")?.extract()?;
        // Finally, push and store the mutable reference
        variable_refs.insert(var_name, py_cell);
    }
    // Return the ref
    Ok(variable_refs)
}

pub fn convert_to_constraint_ref(variables: &PyAny) -> Result<Vec<PyRefMut<Constraint>>, PyErr> {
    // Convert the PyAny into a PyList
    let variables_list: &PyList = variables.downcast()?;

    // Create the vector to store this references
    let mut constraint: Vec<PyRefMut<Constraint>> = Vec::new();

    // Iterate over the elements in the PyList
    for item in variables_list.iter() {
        // convert the item into a cell of type &PyCell<EngineVar>
        let py_cell: &PyCell<Constraint> = item.downcast()?;

        // Finally, push and store the mutable reference
        constraint.push(py_cell.borrow_mut());
    }
    // Return the ref
    Ok(constraint)
}

pub fn generate_solution_combinations(
    vars: &HashMap<&str, &PyCell<EngineVar>>,
) -> MultiProduct<IntoIter<f64>> {
    let mut all_values: Vec<Vec<f64>> = Vec::new();
    for var in vars.values() {
        let engine_var = var.borrow();
        let values = engine_var.solution_space();
        all_values.push(values);
    }
    // Generate all the combinations using the cartesian product
    let result = all_values.iter().cloned().multi_cartesian_product();
    // Return the value converted to
    result
}
