/// Utilities without an specific function
///
use itertools::{Itertools, MultiProduct};
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};
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

pub fn update_results(results: &PyDict, vars: &HashMap<&str, &PyCell<EngineVar>>) -> PyResult<()> {
    // Update the
    for (py_ind, py_val) in results {
        // Convert the PyObject `var_ind` into a usize
        let var_ind: &str = py_ind.extract()?;
        // Convert the PyObject `value` into a f64
        let value: f64 = py_val.extract()?;
        // Using the var index, search the solution dict
        if let Some(py_cell) = vars.get(&var_ind) {
            // Borrow the cell
            let mut variable = py_cell.borrow_mut();
            // Set the new value
            variable.set_value(value);
        }
    }
    // Return nothing
    Ok(())
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
