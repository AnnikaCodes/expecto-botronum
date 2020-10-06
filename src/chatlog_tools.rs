/// src/chatlogger.rs
/// Contains functions to manipulate Pokémon Showdown chatlogs stored in SQLite
///
/// Written by Annika

use std::time::{SystemTime, UNIX_EPOCH};

use chrono::prelude::NaiveDateTime;
use rusqlite::{Connection, params};


#[derive(Debug)]
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
#[derive(Debug)]
pub struct LogEntry {
    time: i32,
    /// "chat" or "pm"
    kind: String,
    /// A Pokémon Showdown ID. See the PS source code for what this means.
    sender_id: String,
    sender_name: String,
    body: String,
}

/// Gets the number of seconds since the UNIX epoch as an i64
pub fn unix_time() -> i64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs() as i64
}

/// Logs a Pokémon Showdown chat message (or PM!) to a SQLite database.
///
/// # Example
/// ```
/// let message = chatlog_tools::LogEntry {
///     time: chatlog_tools::unix_time(),
///     kind: String::from("chat"),
///     sender_id: String::from("annika"),
///     sender_name: String::from("@Annika"),
///     body: String::from("hi"),
/// };
/// let my_connection = rusqlite::Connection::open_in_memory().unwrap()
///
/// chatlog_tools::log_message(my_conncetoin, "development", message);
/// ```
pub fn log_message(conn: &Connection, room: &str, message: LogEntry) -> Result<(), rusqlite::Error> {
    if message.kind != "chat" && message.kind != "pm" {
        return Ok(());
    }

    let mut statement = conn.prepare(
        "INSERT INTO logs (timestamp, userid, username, type, roomid, body) VALUES (?, ?, ?, ?, ?, ?)"
    )?;


    statement.execute(params![
        SQLParameter::Number(message.time),
        message.sender_id,
        message.sender_name,
        message.kind,
        room,
        message.body,
    ])?;

    Ok(())
}

/// Searches logs based on a variety of parameters.
/// Output is formatted as HTML suitable for a Pokémon Showdown HTML box
pub fn search(
    conn: &Connection, room_id: &str, user_id: Option<&str>,
    oldest: Option<i32>, keywords: Option<Vec<&str>>, max_messages: Option<i32>
) -> Result<String, rusqlite::Error> {
    let ranks = vec!['+', '^', '%', '@', '*', '#', '&', '~'];

    let mut query_str = String::from("SELECT * FROM logs WHERE roomid = ?");
    let mut args = Vec::<SQLParameter>::new();
    args.push(SQLParameter::Text(room_id.to_owned()));

    if let Some(id) = user_id {
        query_str.push_str(" AND userid = ?");
        args.push(SQLParameter::Text(id.to_owned()));
    }

    if let Some(keywords) = keywords {
        for keyword in keywords {
            query_str.push_str(" AND lower(body) LIKE '%' || ? || '%'");
            args.push(SQLParameter::Text(String::from(keyword).to_lowercase()));
        }
    }

    query_str.push_str(" AND timestamp > ? ORDER BY timestamp DESC LIMIT ?");
    args.push(SQLParameter::Number(oldest.unwrap_or(0)));
    args.push(SQLParameter::Number(max_messages.unwrap_or(1000)));

    let mut statement = conn.prepare(&query_str)?;

    let mut messages_so_far = 0;
    // See https://github.com/hoodie/concatenation_benchmarks-rs for information on
    // string concatenation performance in Rust.
    // TL;DR .join()ing arrays or using push_str with a set-capacity String are best
    let mut html = String::with_capacity(100000);
    let mut rows = statement.query(args)?;
    let mut current_day = String::from("");
    while let Some(row) = rows.next()? {
        // row.get(1) -> timestamp
        let date = NaiveDateTime::from_timestamp(row.get(1).unwrap_or_else(|_| unix_time()), 0);
        let mdy = date.format("%v").to_string();
        if current_day != mdy {
            html.push_str(&[
                if !current_day.is_empty() {
                    "</div></details>"
                } else {
                    ""
                },
                r#"<details style="margin-left: 5px;"><summary><b>"#,
                &mdy,
                r#"</b></summary><div style="margin-left: 10px;">"#,
            ].join(""));
        }

        // row.get(3) -> sender_name
        let mut user: String = row.get(3)?;
        if ranks.contains(&user.chars().next().unwrap()) {
            user = [
                "<small>",
                &html_escape::encode_text(&user[0..1]),
                "</small><b>",
                &html_escape::encode_text(&user[1..]),
                "</b>",
            ].join("");
        } else {
            user = [
                "<b>",
                &user,
                "</b>",
            ].join("");
        }

        // format: <small>[XX:YY:ZZ]</small> user: xyzzy
        html.push_str(&[
            "<small>[",
            &html_escape::encode_text(&date.format("%T").to_string()),
            "] </small>",
            &user,
            ": ",
            &(row.get(6).unwrap_or_else(|_| String::from("")) as String)
        ].join(""));

        if current_day != mdy {
            current_day = mdy;
        }
    }
    html.push_str("</div></details>");
    Ok(html)
}

pub fn get_linecount(conn: &Connection, user_id: &str, room_id: &str, days: Option<i32>) -> Result<i32, rusqlite::Error> {
    let days = days.unwrap_or(30);

    let max_timestamp = unix_time() - (days * 24 * 60 * 60) as i64;
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
            body: String::from("Hello from Rust!"),
            kind: String::from("chat"),
            sender_id: String::from("annika"),
            sender_name: String::from("@Annika"),
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

    #[test]
    fn search_test() -> Result<(), rusqlite::Error> {
        let conn = get_connection();

        log_message(&conn, "test", LogEntry {
            body: String::from("Test Message One"),
            kind: String::from("chat"),
            sender_id: String::from("annika"),
            sender_name: String::from("@Annika"),
            time: 1,
        })?;
        log_message(&conn, "test", LogEntry {
            body: String::from("Test Message Two"),
            kind: String::from("chat"),
            sender_id: String::from("annika"),
            sender_name: String::from("@Annika"),
            time: 1,
        })?;
        log_message(&conn, "someotherroom", LogEntry {
            body: String::from("Test One"),
            kind: String::from("chat"),
            sender_id: String::from("heartofetheria"),
            sender_name: String::from("Heart of Etheria"),
            time: 100,
        })?;
        log_message(&conn, "test", LogEntry {
            body: String::from("Test Two"),
            kind: String::from("chat"),
            sender_id: String::from("heartofetheria"),
            sender_name: String::from("Heart of Etheria"),
            time: 100,
        })?;

        let mut statement = conn.prepare("SELECT * FROM logs").unwrap();
        let mut rows = statement.query(rusqlite::NO_PARAMS).unwrap();
        while let Some(row) = rows.next()? {
            println!("{:?} {:?}", row.get::<usize, String>(2)?, row.get::<usize, String>(5)?);
        };

        // Check that it can search by user ID and format regular users
        let mut results = search(&conn, "test", Some("heartofetheria"), Some(0), None, Some(1000))?;
        assert_eq!(results, "<details style=\"margin-left: 5px;\"><summary><b> 1-Jan-1970</b></summary><div style=\"margin-left: 10px;\"><small>[00:01:40] </small><b>Heart of Etheria</b>: Test Two</div></details>");

        // Check that it can format auth correctly
        results = search(&conn, "test", Some("annika"), Some(0), None, Some(1000))?;
        assert_eq!(results, "<details style=\"margin-left: 5px;\"><summary><b> 1-Jan-1970</b></summary><div style=\"margin-left: 10px;\"><small>[00:00:01] </small><small>@</small><b>Annika</b>: Test Message One<small>[00:00:01] </small><small>@</small><b>Annika</b>: Test Message Two</div></details>");

        // Check that it can search by time
        results = search(&conn, "test", None, Some(50), None, Some(1000))?;
        println!("{}", results);
        assert_eq!(results.contains("Test Two"), true);
        assert_eq!(results.contains("Test Message One"), false);
        assert_eq!(results.contains("Test Message Two"), false);

        // Check that it can limit the number of messages returned
        results = search(&conn, "test", None, None, None, Some(1))?;
        assert_eq!(results.contains("Test Two"), true);
        assert_eq!(results.contains("Test Message One"), false);
        assert_eq!(results.contains("Test Message Two"), false);

        // Check that it can search by a (case-insensitive) keyword
        results = search(&conn, "test", None, None, Some(vec!["tWo"]), None)?;
        assert_eq!(results.contains("Test Two"), true);
        assert_eq!(results.contains("Test Message One"), false);
        assert_eq!(results.contains("Test Message Two"), true);

        Ok(())
    }
}