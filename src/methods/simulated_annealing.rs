//! Simulated Annealing method
//!
//! Provided a `SA` implementation that allow the calls of soft and hard constraints.
//!

use pyo3::prelude::*;
use pyo3::types::{PyDict, PyFloat};
// Extra import
use rand::Rng;
// Use the engine variable

#[derive(Debug, PartialEq)]
pub enum Number {
    Integer(i64),
    Float(f64),
}

// SA parameters
const INITIAL_TEMPERATURE: f64 = 1000.0;
const COOLING_RATE: f64 = 0.95;
const MAX_ITERATIONS: usize = 10;

/// Simulated Annealing
#[pyfunction]
pub fn simulated_annealing(
    py: Python,
    variables: Vec<&PyAny>,
    constraints: Vec<&PyAny>,
    cost_method: PyObject,
) -> PyResult<&'static str> {
    let mut rng = rand::thread_rng();
    // Init some parameters, such as the temperature and others
    let mut status = "UNFEASIBLE";

    // Define el estilo de la barra de progreso
    // pb.set_style(
    //     ProgressStyle::default_bar()
    //         .template("{bar:40.cyan/blue} {percent:>3}%")
    //         .progress_chars("##-"),
    // );
    // Define a hint solution
    let best_solution = hint_solution(py, &variables)?;
    let current_solution = best_solution.as_ref(py);
    let best_cost: f64 = calculate_cost(py, &current_solution, &cost_method, &constraints)?;
    // Define some SA parameters
    let mut temperature = INITIAL_TEMPERATURE;
    // Start the optimization
    while temperature > 1e-6 {
        for _ in 0..MAX_ITERATIONS {
            // Generate a neighborhood solution
            let (neigh_var, neigh_value) = neighborhood_solution(py, &variables)?;
            let _ = current_solution.set_item(neigh_var, neigh_value);
            // Calculate the cost for the new solution
            let new_cost: f64 = calculate_cost(py, &current_solution, &cost_method, &constraints)?;
            // Evaluate their diff
            let cost_diff = f64::max(0.0, best_cost - new_cost);
            // Obtain the metropolis prob
            let random_val: f64 = rng.gen();
            let metropolis_prob = random_val < (-(cost_diff) / temperature).exp();

            // Check if this is a valid solution
            if cost_diff < 0.0 || metropolis_prob {
                status = "FEASIBLE";
                for variable in &variables {
                    let new_value: f64 = current_solution.get_item(variable).unwrap().extract()?;
                    // Use the setter method to set the new value
                    variable.setattr("value", new_value)?;
                }
            }
        }
        // Reduce the temperature using the cooling rate
        temperature *= COOLING_RATE;
    }
    // Return the status
    Ok(status)
}

/// Calculate the cost of the Python cost function
fn calculate_cost(
    py: Python,
    solution: &PyAny,
    cost_method: &PyObject,
    constraints: &Vec<&PyAny>,
) -> PyResult<f64> {
    let mut cost_constraints = 0.0;
    // Get the constraint values here
    for constraint in constraints {
        let _cost = constraint.call1((solution,))?;
        let cost: f64 = _cost.extract()?;

        cost_constraints = cost_constraints + cost;
    }

    let cost = cost_method.call1(py, (solution,))?;
    let obj_cost: f64 = cost.extract(py)?;
    // Then, get the final cost
    let final_cost: f64;
    if cost_constraints.is_infinite() {
        final_cost = cost_constraints;
    } else {
        final_cost = obj_cost + cost_constraints;
    }
    // let final_cost = obj_cost + cost_constraints;
    Ok(final_cost)
}

/// Generate a hint solution
fn hint_solution(py: Python, variables: &[&PyAny]) -> PyResult<PyObject> {
    // From each variable, create a neighborhood
    let var_values = PyDict::new(py);
    for variable in variables {
        // Create the solution for each one. First, get the neighborhood
        let value = variable_solution(variable)?;
        // Then, set the element in the solution
        let _ = var_values.set_item(variable, convert_number_to_py(py, &value));
    }
    Ok(var_values.to_object(py))
}

fn convert_number_to_py(py: Python, number: &Number) -> PyObject {
    match number {
        Number::Integer(value) => (*value).to_object(py),
        Number::Float(value) => PyFloat::new(py, *value).to_object(py),
    }
}

fn neighborhood_solution<'a>(
    py: Python,
    variables: &'a [&PyAny],
) -> PyResult<(&'a PyAny, PyObject)> {
    let mut rng = rand::thread_rng();
    // Randomly choose one variable
    let index = rng.gen_range(0..variables.len());
    let selected_variable = variables[index];
    // From here, get the variable solution
    let value = convert_number_to_py(py, &variable_solution(selected_variable)?);
    // And return both
    Ok((selected_variable, value))
}

fn variable_solution(variable: &PyAny) -> PyResult<Number> {
    // Instance the random structure
    let mut rng = rand::thread_rng();
    // Obtain their lower and upper limit
    let (lb, ub) = obtain_var_bounds(variable)?;
    if lb == ub {
        return Ok(lb);
    }
    // With this, generate a random number between these two
    let value = match (lb, ub) {
        (Number::Integer(lb), Number::Integer(ub)) => Number::Integer(rng.gen_range(lb..=ub)),
        (Number::Float(lb), Number::Float(ub)) => Number::Float(rng.gen_range(lb..ub)),
        (Number::Integer(lb), Number::Float(ub)) => Number::Float(rng.gen_range(lb as f64..ub)),
        (Number::Float(lb), Number::Integer(ub)) => Number::Float(rng.gen_range(lb..ub as f64)),
    };

    Ok(value)
}

fn obtain_var_bounds(variable: &PyAny) -> PyResult<(Number, Number)> {
    let lb = variable.getattr("lower_bound")?;
    let ub = variable.getattr("upper_bound")?;

    // Convert lb into a float or into an integer
    let lb = if let Ok(value) = lb.extract() {
        Number::Integer(value)
    } else {
        Number::Float(lb.extract()?)
    };
    // Convert now ub into a float or into an integer
    let ub = if let Ok(value) = ub.extract() {
        Number::Integer(value)
    } else {
        Number::Float(ub.extract()?)
    };

    Ok((lb, ub))
}
