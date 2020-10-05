/// src/chatlogger.rs
/// Contains functions to manipulate Pokémon Showdown chatlogs stored in SQLite
///
/// Written by Annika

use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};

use chrono::prelude::NaiveDateTime;

use rusqlite::{Connection, params};

/// Gets the number of seconds since the UNIX epoch
fn unix_time() -> i32 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs() as i32
}

enum SQLParameter {
    Number(i32),
    Text(String),
    Null,
}

impl rusqlite::ToSql for SQLParameter {
    fn to_sql(&self) -> Result<rusqlite::types::ToSqlOutput, rusqlite::Error> {
        match self {
            Self::Number(n) => n.to_sql(),
            Self::Text(s) => s.to_sql(),
            Self::Null => rusqlite::types::Null.to_sql(),
        }
    }
}

/// Rustic version of the "userid|time|kind|senderName|body" log format
pub struct LogEntry {
    time: i32,
    /// "chat" or "pm"
    kind: String,
    sender_id: Option<String>,
    sender_name: Option<String>,
    body: Option<String>,
}

pub fn log_message(conn: &Connection, room: &str, message: LogEntry) -> Result<(), rusqlite::Error> {
    if message.kind != "chat" && message.kind != "pm" {
        return Ok(());
    }

    let mut statement = conn.prepare(
        "INSERT INTO logs (timestamp, userid, username, type, roomid, body) VALUES (?, ?, ?, ?, ?, ?)"
    )?;


    statement.execute(params![
        SQLParameter::Number(message.time),
        match message.sender_id {
            Some(m) => SQLParameter::Text(m),
            None => SQLParameter::Null,
        },
        match message.sender_name {
            Some(m) => SQLParameter::Text(m),
            None => SQLParameter::Null,
        },
        message.kind,
        room,
        message.body,
    ])?;

    Ok(())
}

/// Searches logs based on a variety of parameters
pub fn search(
    conn: Connection,
    room_id: &str, user_id: Option<&str>,
    oldest: Option<i32>, keywords: Option<Vec<&str>>
) -> Result<HashMap<String, Vec<LogEntry>>, rusqlite::Error> {
    let oldest = oldest.unwrap_or(0);
    let keywords = keywords.unwrap_or_else(|| [].to_vec());

    let mut results = HashMap::<String, Vec<LogEntry>>::new();

    let mut query_str = String::from("SELECT * FROM logs WHERE roomid = ?");
    let mut args = Vec::<SQLParameter>::new();
    args.push(SQLParameter::Text(room_id.to_owned()));

    if let Some(id) = user_id {
        query_str.push_str(" AND userid = ?");
        args.push(SQLParameter::Text(id.to_owned()));
    }

    for keyword in keywords.iter() {
        query_str.push_str(" AND lower(body) LIKE '%' || ? || '%'");
        args.push(SQLParameter::Text(String::from(*keyword).to_lowercase()));
    }

    query_str.push_str(" AND timestamp > ? ORDER BY timestamp DESC");
    args.push(SQLParameter::Number(oldest));

    let mut statement = conn.prepare(&query_str)?;

    statement.query_map(args, |row| {
        let date = NaiveDateTime::from_timestamp(row.get(1)?, 0).format("%Y-%m-%d");

        results.entry(date.to_string()).or_insert(Vec::<LogEntry>::new());
        results.get_mut(&date.to_string()).unwrap().push(LogEntry {
            time: row.get(1)?,
            sender_id: row.get(2)?,
            sender_name: row.get(3)?,
            kind: row.get(4)?,
            body: row.get(6)?,
        });
        Ok(())
    })?;
    Ok(results)
}

pub fn get_linecount(conn: Connection, user_id: &str, room_id: &str, days: Option<i32>) -> Result<i32, rusqlite::Error> {
    let days = days.unwrap_or(30);

    let max_timestamp = unix_time() - days * 24 * 60 * 60;
    let mut statement = conn.prepare("SELECT count(log_id) FROM logs WHERE userid = ? AND roomid = ? AND timestamp > ?")?;
    statement.query_row(params![user_id, room_id, max_timestamp], |row| row.get(0))
}

#[cfg(test)]
mod tests {
    use super::*;
    fn get_connection() -> Connection {
        let connection = Connection::open_in_memory().unwrap();
        connection.execute(
            "CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER NOT NULL PRIMARY KEY,
                -- UNIX timestamp
                timestamp INTEGER NOT NULL,
                -- the ID of the user who sent the message
                userid TEXT,
                -- their name
                username TEXT,
                -- chat, pm, etc
                type TEXT NOT NULL,
                -- null if it's a PM/other global message
                roomid TEXT,
                body TEXT
            );

            CREATE INDEX IF NOT EXISTS log_index_1 ON logs(timestamp);
            CREATE INDEX IF NOT EXISTS log_index_2 ON logs(userid, timestamp);
            CREATE INDEX IF NOT EXISTS log_index_3 ON logs(userid, roomid, timestamp);
            CREATE INDEX IF NOT EXISTS log_index_5 ON logs(type, userid, roomid, timestamp);
            PRAGMA journal_mode=WAL;",
            rusqlite::NO_PARAMS
        ).unwrap();
        connection
    }

    #[test]
    fn insertion_test() -> Result<(), rusqlite::Error> {
        let conn = get_connection();
        log_message(&conn, "test", LogEntry {
            body: Some(String::from("Hello from Rust!")),
            kind: String::from("chat"),
            sender_id: Some(String::from("annika")),
            sender_name: Some(String::from("@Annika")),
            time: 1601875655,
        })?;

        conn.query_row("SELECT * FROM logs", rusqlite::NO_PARAMS, |row: &rusqlite::Row| {
            assert_eq!(row.get::<usize, i32>(1).unwrap(), 1601875655);
            assert_eq!(row.get::<usize, String>(2).unwrap(), String::from("annika"));
            assert_eq!(row.get::<usize, String>(3).unwrap(), String::from("@Annika"));
            assert_eq!(row.get::<usize, String>(4).unwrap(), String::from("chat"));
            assert_eq!(row.get::<usize, String>(5).unwrap(), String::from("test"));
            assert_eq!(row.get::<usize, String>(6).unwrap(), String::from("Hello from Rust!"));
            Ok(())
        })?;
        Ok(())
    }
}