/// Include several optimization techniques.
/// For this module, the techniques are of type `search`,
/// since we're searching.
///
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::PyResult;
use std::time::Instant;
// Local imports
use crate::math_utilities::{
    convert_to_constraint_ref, convert_to_var_ref, generate_solution_combinations, update_results,
};
use crate::model::Constraint;

#[pyfunction]
#[allow(unused_assignments)]
pub fn brute_force(
    py: Python,
    variables: &PyAny,
    constraints: &PyAny,
    objective: PyObject,
    // Extra methods, such as solver time
    solver_time: f64,
) -> PyResult<&'static str> {
    let mut status = "UNFEASIBLE";
    // Get the mut variables
    let ref_vars = convert_to_var_ref(variables)?;
    let ref_const = convert_to_constraint_ref(constraints)?;
    //
    let variable_names: Vec<&str> = ref_vars.keys().cloned().collect();

    // Create the best solution and best cost
    let mut best_cost = (2147483647, f64::INFINITY);
    // From here, evaluate each one of the solutions to search for the best solution
    let timer = Instant::now();
    let mut timeout = timer.elapsed().as_secs_f64();
    while timeout < solver_time {
        // Get the number of elements and number of combinations
        let combinations = generate_solution_combinations(&ref_vars);
        for combination in combinations {
            timeout = timer.elapsed().as_secs_f64();
            // Create the current solution over here
            let current_solution = PyDict::new(py);
            // Set the variable values for this combination
            for (i, value) in combination.iter().enumerate() {
                let var_name = variable_names.get(i).ok_or_else(|| {
                    PyErr::new::<pyo3::exceptions::PyIndexError, _>(
                        "Index out of bounds when retrieving variable name",
                    )
                })?;

                if let Some(var) = ref_vars.get(var_name) {
                    let _ = current_solution.set_item(var.getattr("name")?, *value);
                }
            }
            // Evaluate the current cost
            let current_cost =
                evaluate_constraints_and_objective(py, current_solution, &ref_const, &objective)?;

            // With this current cost, evaluate if this is lower than the best cost
            if current_cost < best_cost {
                status = "FEASIBLE";
                // Make the current cost now the best cost
                best_cost = current_cost;
                println!(
                    "Solution found at {}s with cost {}",
                    timer.elapsed().as_secs_f64(),
                    best_cost.1
                );
                // Iterate over the var and values to update them
                update_results(current_solution, &ref_vars)?;
            }
        }
        status = "OPTIMAL"; // * If the brute force ends, then we know that we'll
    }
    // Return the status at the very end
    Ok(status)
}

// ============================== //
//         Extra methods          //
// ============================== //

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
