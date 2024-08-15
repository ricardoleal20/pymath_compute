use pyo3::prelude::*;
use pyo3::types::PyDict;
use rand::Rng;
use std::collections::HashMap;
use std::time::Instant;
// Extra import
use crate::math_utilities::{convert_to_constraint_ref, convert_to_var_ref, update_results};
use crate::model::{Constraint, EngineVar};

// SA parameters
const INITIAL_TEMPERATURE: f64 = 1000.0;
const COOLING_RATE: f64 = 0.95;
const MAX_ITERATIONS: usize = 1000;

/// Simulated Annealing function
/// Receives
#[pyfunction]
pub fn simulated_annealing(
    py: Python,
    variables: &PyAny,
    constraints: &PyAny,
    objective: PyObject,
    // Extra methods, such as solver time
    solver_time: f64,
) -> PyResult<&'static str> {
    // Init the random generator
    let mut rng = rand::thread_rng();
    let mut status = "UNFEASIBLE";
    // Get the mut variables
    let ref_vars = convert_to_var_ref(variables)?;
    let ref_const = convert_to_constraint_ref(constraints)?;
    // Get the keys of the reference vars
    let keys: Vec<&str> = ref_vars.keys().cloned().collect();
    // Generate a hint solution and a best cost
    let hint = hint_solution(py, &ref_vars)?;
    let mut best_solution = hint.extract(py)?;
    let mut best_cost =
        evaluate_constraints_and_objective(py, best_solution, &ref_const, &objective)?;
    // Define the temperature
    let mut temperature = INITIAL_TEMPERATURE;
    // Start the timing count
    let timer = Instant::now();
    let mut timeout = timer.elapsed().as_secs_f64();
    // Start the optimization process
    while temperature > 1e-3 && timeout < solver_time {
        // Create a copy of the best solution
        let current_solution = best_solution.copy()?;
        for _ in 0..MAX_ITERATIONS {
            // Update the time
            timeout = timer.elapsed().as_secs_f64();
            // Generate a neighborhood solution. For this, randomly select a var from the keys
            let selected_var_name = keys[rng.gen_range(0..keys.len())];
            let selected_var = ref_vars[selected_var_name];
            // Create a solution for this var
            let new_solution = variable_solution(selected_var);
            // Set this on the current solution parameter
            let _ = current_solution.set_item(selected_var_name, new_solution);
            // Evaluate the cost
            let current_cost =
                evaluate_constraints_and_objective(py, current_solution, &ref_const, &objective)?;
            // Obtain the metropolis prob
            let random_val: f64 = rng.gen();
            let metropolis_prob =
                random_val < (-(f64::max(0.0, best_cost.1 - current_cost.1)) / temperature).exp();

            // Evaluate if this is better
            if current_cost < best_cost || metropolis_prob {
                // Update all the elements
                if current_cost.0 == 0 && current_cost.1 <= best_cost.1 {
                    status = "FEASIBLE";
                    println!(
                        "Solution found at {}s with cost {}",
                        timer.elapsed().as_secs_f64(),
                        current_cost.1
                    );
                    // Update the best solution
                    best_solution = current_solution;
                }
                // Update the cost
                best_cost = current_cost;
            }
        }
        // Reduce the temperature using the cooling rate
        temperature *= COOLING_RATE;
    }
    // If the status is other than "UNFEASIBLE"
    if status != "UNFEASIBLE" {
        update_results(best_solution, &ref_vars)?;
    }
    // Return the status
    Ok(status)
}

// ========================== //
//       Extra methods        //
// ========================== //
fn hint_solution(
    py: Python,
    variables: &HashMap<&str, &PyCell<EngineVar>>,
) -> PyResult<Py<PyDict>> {
    // Create the dictionary
    let solution = PyDict::new(py);
    // From here, iterate over all the variables
    for (var_name, variable) in variables {
        // Generate a random solution
        let random_space_solution = variable_solution(variable);
        // Set the value for this var and pretend that this is the solution
        let _ = solution.set_item(var_name, random_space_solution);
    }
    // Return the solution
    Ok(solution.into())
}

fn variable_solution(variable: &PyCell<EngineVar>) -> f64 {
    // Initialize the random generator
    let mut rng = rand::thread_rng();
    // Borrow the engine var
    let engine_var = variable.borrow();
    // From the EngineVar, get the solution space
    let space = engine_var.solution_space();
    // Select a random value from this space and return it
    let index = rng.gen_range(0..space.len());
    space[index]
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
