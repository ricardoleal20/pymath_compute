use std::collections::HashMap;
use std::hash::Hash;

/// Include several optimization techniques.
/// For this module, the techniques are of type `search`,
/// since we're searching.
///
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::PyResult;
// Local imports
use crate::math_utilities::{
    convert_to_constraint_ref, convert_to_var_ref, generate_solution_combinations,
};
use crate::model::Constraint;

#[pyfunction]
pub fn held_karp(_py: Python, variables: &PyAny, constraints: &PyAny) -> PyResult<&'static str> {
    // Provide the status
    let status = "UNFEASIBLE";
    // Get the mut variables and constraints
    let ref_vars = convert_to_var_ref(variables)?;
    let ref_const = convert_to_constraint_ref(constraints)?;
    // Get the variable names
    let variable_names: Vec<&str> = ref_vars.keys().cloned().collect();
    let n_variables = variable_names.len();
    // Create the distances matrix
    let distances_matrix = build_distance_matrix(n_variables, &ref_const);
    // Create the best solution and best cost
    let mut best_cost = (2147483647, f64::INFINITY);
    // Create the HashMap of visited cities
    let nodes_visited: HashMap<i32, HashMap<i32, i32>> = HashMap::new();
    // Iterate over all the variables
    for (prev_var_name, prev_var) in &ref_vars {
        for (next_var_name, next_var) in &ref_vars {
            if prev_var_name == next_var_name {
                continue;
            }
        }
    }
    // Return the status at the very end
    Ok(status)
}

#[pyfunction]
pub fn brute_force(
    py: Python,
    variables: &PyAny,
    constraints: &PyAny,
    objective: PyObject,
) -> PyResult<&'static str> {
    let mut status = "UNFEASIBLE";
    // Get the mut variables
    let rev_vars = convert_to_var_ref(variables)?;
    let ref_const = convert_to_constraint_ref(constraints)?;
    //
    let variable_names: Vec<&str> = rev_vars.keys().cloned().collect();

    // Create the best solution and best cost
    let mut best_cost = (2147483647, f64::INFINITY);
    // Get the number of elements and number of combinations
    let combinations = generate_solution_combinations(&rev_vars);
    // From here, evaluate each one of the solutions to search for the best solution
    for combination in combinations {
        // Create the current solution over here
        let current_solution = PyDict::new(py);
        // Set the variable values for this combination
        for (i, value) in combination.iter().enumerate() {
            let var_name = variable_names.get(i).ok_or_else(|| {
                PyErr::new::<pyo3::exceptions::PyIndexError, _>(
                    "Index out of bounds when retrieving variable name",
                )
            })?;

            if let Some(var) = rev_vars.get(var_name) {
                let _ = current_solution.set_item(var.getattr("name")?, *value);
            }
        }
        // Evaluate the current cost
        let current_cost =
            evaluate_constraints_and_objective(py, current_solution, &ref_const, &objective)?;

        // println!("OldCost={:?} vs NewCost={:?}", best_cost, current_cost);
        // With this current cost, evaluate if this is lower than the best cost
        if current_cost < best_cost {
            status = "OPTIMAL";
            // Make the current cost now the best cost
            best_cost = current_cost;
            // Iterate over the var and values to update them
            for (py_ind, py_val) in current_solution {
                // Convert the PyObject `var_ind` into a usize
                let var_ind: &str = py_ind.extract()?;
                // Convert the PyObject `value` into a f64
                let value: f64 = py_val.extract()?;
                // Using the var index, search the solution dict
                if let Some(py_cell) = rev_vars.get(&var_ind) {
                    // Borrow the cell
                    let mut variable = py_cell.borrow_mut();
                    // Set the new value
                    variable.set_value(value);
                }
            }
        }
    }
    // Return the status at the very end
    Ok(status)
}

// ============================== //
//         Extra methods          //
// ============================== //
fn build_distance_matrix(
    n_of_elements: usize,
    constraints: &Vec<PyRefMut<Constraint>>,
) -> Vec<Vec<f64>> {
    // Create the matrix
    let mut distances = vec![vec![f64::INFINITY; n_of_elements]; n_of_elements];
    // Iterate over the number of elements
    for i in 0..n_of_elements {
        for j in 0..n_of_elements {
            // If i == j, then continue
            if i == j {
                continue;
            }
            // If not, then build the new distance element
            let dist_key = format!("DIST_{}_{}", i, j);
            if let Some(&constraint) = constraints.get(&dist_key) {
                // Set this constraint element as an distance
                distances[i][j] = constraint;
            }
        }
    }
    // Return the matrix
    distances
}

// ============================== //
//      Evaluation methods        //
// ============================== //
fn evaluate_constraints_and_objective(
    py: Python,
    current_solution: &PyDict,
    constraints: &Vec<PyRefMut<Constraint>>,
    objective: &PyObject,
) -> Result<(i32, f64), PyErr> {
    let mut cost: f64 = 0.0;
    let mut hard_constraints: i32 = 0;
    // Iterate over the constraints to evaluate it
    for constraint in constraints {
        // Evaluate the cost for this constraint
        let constraint_cost = constraint.value(py, Some(current_solution))?;
        if constraint_cost == f64::INFINITY {
            hard_constraints += 1
        } else {
            cost += constraint_cost
        }
    }

    // Evaluate the objective
    let objective_evaluation: Py<PyAny> = objective.call1(py, (current_solution,))?;
    let objective_cost: f64 = objective_evaluation.extract(py)?;
    // At the end, return the tuple of the hard constraints found and the total cost
    Ok((hard_constraints, cost + objective_cost))
}
