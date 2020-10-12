/// src/lib.rs
///
/// This file wraps chatlog_tools so that Python can access it
///
/// Written by Annika (who is still fairly new to Rust :p)

use pyo3::prelude::*;
use pyo3::create_exception;
use rusqlite::*;

pub mod chatlog_tools;

create_exception!(rust_chatlog, RustError, pyo3::exceptions::Exception);

/// Converts a Rust-based error to a Python exception (RustError)
/// See https://pyo3.rs/v0.10.1/exception.html
fn pythonize_exception(exception: Box<dyn std::error::Error>) -> PyErr {
    RustError::py_err(exception.to_string())
}

#[pymodule]
fn rust_chatlogger(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Chatlogger>()?;
    Ok(())
}

#[pyclass]
#[derive(Clone, Debug)]
struct Chatlogger {
    path: String, // We have to create a connection on each query since rusqlite::Connection can't be cloned
}

#[pymethods]
impl Chatlogger {
    #[new]
    fn new(path: String) -> Self {
        Chatlogger { path }
    }

    /// Handles incoming messages
    fn handle_message(
        self_: PyRef<Self>, kind: String, room_id: Option<&str>, timestamp: Option<i32>,
        sender_id: String, sender_name: String, body: String,
    ) -> PyResult<()> {
        RustError::py_err("Hello from Rust!");
        let conn = match Connection::open(&self_.path) {
            Ok(c) => c,
            Err(e) => return Err(pythonize_exception(Box::new(e))),
        };

        let entry = chatlog_tools::LogEntry {
            time: timestamp.unwrap_or(chatlog_tools::unix_time() as i32),
            kind,
            sender_id,
            sender_name,
            body,
        };

        match chatlog_tools::log_message(&conn, room_id.unwrap_or("global"), entry) {
            Ok(c) => c,
            Err(e) => return Err(pythonize_exception(Box::new(e))),
        };
        match conn.close() {
            Ok(c) => c,
            Err((_, e)) => return Err(pythonize_exception(Box::new(e))),
        };
        Ok(())
    }

    /// Searches the database for chat messages and returns a HTML response.
    fn html_search(
        self_: PyRef<Self>, room_id: &str, user_id: Option<&str>,
        oldest: Option<i32>, keywords: Option<Vec<&str>>, max_messages: Option<i32>
    ) -> PyResult<String> {
        let conn = match Connection::open(&self_.path) {
            Ok(c) => c,
            Err(e) => return Err(pythonize_exception(Box::new(e))),
        };

        let html = match chatlog_tools::search(&conn, room_id, user_id, oldest, keywords, max_messages) {
            Ok(h) => h,
            Err(e) => return Err(pythonize_exception(Box::new(e))),
        };

        match conn.close() {
            Ok(c) => c,
            Err((_, e)) => return Err(pythonize_exception(Box::new(e))),
        };
        Ok(html)
    }

    /// Gets a user's linecount as HTML
    fn linecount_html(self_: PyRef<Self>, room_id: &str, user_id: &str, days: Option<i32>) -> PyResult<String> {
        let conn = match Connection::open(&self_.path) {
            Ok(c) => c,
            Err(e) => return Err(pythonize_exception(Box::new(e))),
        };

        let result = match chatlog_tools::get_linecount_html(&conn, user_id, room_id, days) {
            Ok(h) => h,
            Err(e) => return Err(pythonize_exception(Box::new(e))),
        };

        match conn.close() {
            Ok(c) => c,
            Err((_, e)) => return Err(pythonize_exception(Box::new(e))),
        };
        Ok(result)
    }

    fn topusers_html(self_: PyRef<Self>, room_id: &str, days: Option<i32>, num_users: Option<i32>) -> PyResult<String> {
        let conn = match Connection::open(&self_.path) {
            Ok(c) => c,
            Err(e) => return Err(pythonize_exception(Box::new(e))),
        };

        let html = match chatlog_tools::get_topusers_html(&conn, room_id, days, num_users) {
            Ok(h) => h,
            Err(e) => return Err(pythonize_exception(Box::new(e))),
        };

        match conn.close() {
            Ok(c) => c,
            Err((_, e)) => return Err(pythonize_exception(Box::new(e))),
        };
        Ok(html)
    }
}

