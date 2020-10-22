/// benches/benchmarks.rs
/// Contains benchmakrs for chatlog_tools
/// Written by Annika
#[macro_use]
extern crate bencher;

#[path = "../src/chatlog_tools.rs"]
mod chatlog_tools;

use rusqlite::*;
use bencher::{Bencher};

fn add_messages(conn: &Connection, num_messages: i32, override_id: bool) -> Result<(), rusqlite::Error> {
    let current_time = chatlog_tools::unix_time() as i32;
    let mut added = 0;

    while added < num_messages {
        added += 1;
        chatlog_tools::log_message(conn, "benchmark", chatlog_tools::LogEntry {
            body: added.to_string(),
            kind: String::from("benchmark"),
            sender_id: if override_id { (added % 1000).to_string() } else { String::from("heartofetheria") },
            sender_name: String::from("Heart of Etheria"),
            time: current_time - added,
        })?;
    }
    Ok(())
}


fn insert_100_messages_benchmark(b: &mut Bencher) {
    let conn = chatlog_tools::tests::get_connection();
    b.iter(|| add_messages(&conn, 100, false));
}

fn search_100k_messages_benchmark(b: &mut Bencher) {
    let conn = chatlog_tools::tests::get_connection();
    add_messages(&conn, 100000, false).unwrap(); // 100k messages
    b.iter(|| {
        chatlog_tools::search(
            &conn, "benchmark", Some("heartofetheria"),
            None, Some(vec!["1"]), None
        )
    });
}

fn linecount_100k_messages_benchmark(b: &mut Bencher) {
    let conn = chatlog_tools::tests::get_connection();
    add_messages(&conn, 100000, false).unwrap(); // 100k messages
    b.iter(|| {
        chatlog_tools::get_linecount(
            &conn, "benchmark", "heartofetheria",
            chatlog_tools::unix_time() as i32 - 30 * chatlog_tools::SECONDS_PER_DAY, chatlog_tools::unix_time() as i32
        )
    });
}


fn linecount_html_100k_messages_benchmark(b: &mut Bencher) {
    let conn = chatlog_tools::tests::get_connection();
    add_messages(&conn, 100000, false).unwrap(); // 100k messages
    b.iter(|| {
        chatlog_tools::get_linecount_html(&conn, "benchmark", "heartofetheria", Some(30), None)
    });
}

fn topusers_100k_messages_benchmark(b: &mut Bencher) {
    let conn = chatlog_tools::tests::get_connection();
    add_messages(&conn, 100000, true).unwrap(); // 100k messages
    b.iter(|| {
        chatlog_tools::get_topusers(&conn, "benchmark", Some(30), Some(50))
    });
}

fn topusers_html_100k_messages_benchmark(b: &mut Bencher) {
    let conn = chatlog_tools::tests::get_connection();
    add_messages(&conn, 100000, true).unwrap(); // 100k messages
    b.iter(|| {
        chatlog_tools::get_topusers_html(&conn, "benchmark", Some(30), Some(50))
    });
}

benchmark_group!(benchmarks,
    insert_100_messages_benchmark,
    search_100k_messages_benchmark,
    linecount_100k_messages_benchmark,
    linecount_html_100k_messages_benchmark,
    topusers_100k_messages_benchmark,
    topusers_html_100k_messages_benchmark
);
benchmark_main!(benchmarks);