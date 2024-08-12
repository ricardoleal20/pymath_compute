use pyo3::prelude::*;
use std::collections::hash_map::DefaultHasher;
// Import the hash
use std::hash::{Hash, Hasher};

/// Represents a variable with a specific range [lower_bound, upper_bound]. This is
/// the var used in the engine for all the mathematical operations.
///
/// Attributes:
///     name (str): The name of the variable.
///     lb (f64): The lower bound of the variable's range. Default to -infinite
///     ub (f64): The upper bound of the variable's range. Default to infinite
///     v0 (Optional[f64]): The initial value of the variable
///     only_integer (bool): If this variable can only take integer values or if it can take also float values.
#[pyclass]
#[derive(Clone)]
pub struct EngineVar {
    _name: String,
    pub lower_bound: f64,
    pub upper_bound: f64,
    _value: Option<f64>,
    _is_integer: bool,
    _interval_size: f64,
}

// Implement the hash method for the variable
impl Hash for EngineVar {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self._name.hash(state);
        self.lower_bound.to_bits().hash(state);
        self.upper_bound.to_bits().hash(state);
        self._is_integer.hash(state);
    }
}

#[pymethods]
impl EngineVar {
    #[new]
    fn new(
        name: String,
        lb: Option<f64>,
        ub: Option<f64>,
        v0: Option<f64>,
        only_integer: bool,
    ) -> PyResult<Self> {
        let lb = lb.unwrap_or(f64::NEG_INFINITY);
        let ub = ub.unwrap_or(f64::INFINITY);

        if lb > ub {
            return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                "The lower bound should be lower than the upper bound",
            ));
        }

        if let Some(v0) = v0 {
            if v0 < lb || v0 > ub {
                return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    "The initial value is not within the defined bounds",
                ));
            }
        }
        let interval_size: f64 = if only_integer { 1.0 } else { 0.1 };

        Ok(EngineVar {
            _name: name,
            lower_bound: lb,
            upper_bound: ub,
            _value: v0.or_else(|| {
                if lb == f64::NEG_INFINITY {
                    None
                } else {
                    Some(lb)
                }
            }),
            _is_integer: only_integer,
            _interval_size: interval_size,
        })
    }

    #[getter]
    pub fn name(&self) -> &str {
        &self._name
    }

    #[getter]
    pub fn value(&self) -> f64 {
        self._value.unwrap_or(0.0)
    }

    #[setter]
    pub fn set_value(&mut self, new_value: f64) {
        self._value = Some(match new_value {
            x if x < self.lower_bound => self.lower_bound,
            x if x > self.upper_bound => self.upper_bound,
            _ => new_value,
        });
    }

    #[getter]
    pub fn interval_size(&self) -> f64 {
        self._interval_size
    }

    #[setter]
    pub fn set_interval_size(&mut self, interval_size: f64) {
        self._interval_size = interval_size;
    }

    #[getter]
    pub fn solution_space(&self) -> Vec<f64> {
        let mut space = vec![self.lower_bound];
        let mut value = self.lower_bound + self.interval_size();
        while value <= self.upper_bound {
            space.push(value);
            value += self.interval_size();
        }
        space
    }

    // Hash method for Python
    fn __hash__(&self) -> PyResult<usize> {
        // Create the mutable hash state
        let mut hash_state = DefaultHasher::new();
        self.hash(&mut hash_state);
        // Return the finish state as usize
        Ok(hash_state.finish() as usize)
    }
}
