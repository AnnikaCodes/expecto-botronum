#![allow(non_snake_case)] // for compatibility with the rest of Expecto Botronum
/// src/lib.rs
///
/// This file exposes all public (Rustified) interfaces to the main Python code.
/// Some functions that work with the SQL databases are abstracted in src/chatlogger.rs
///
/// Written by Annika (who is still fairly new to Rust :p)

use pyo3::prelude::*;
use pyo3::create_exception;

mod chatlog_tools;

create_exception!(rust_chatlog, RustError, pyo3::exceptions::Exception);

/// Converts a Rust-based error to a Python exception (RustError)
/// See https://pyo3.rs/v0.10.1/exception.html
fn pythonize_exception(exception: Box<dyn std::error::Error>) -> PyErr {
    RustError::py_err(exception.to_string())
}

