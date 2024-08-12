//! Module implementation of Rust math utilities
//!
//! This module includes:
//!     - Methods to calculate a derivate or a gradient
//!     - Methods to calculate integrals
// Module import
pub mod derivate;
pub mod miscellaneous;
// Make easier the access to the create ref
pub use miscellaneous::{
    convert_to_constraint_ref, convert_to_var_ref, generate_solution_combinations,
};
