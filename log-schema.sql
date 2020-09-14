-- SQLite schema for Expecto Botronum's logs

CREATE TABLE IF NOT EXISTS logs (
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
CREATE INDEX IF NOT EXISTS log_index_4 ON logs(roomid, timestamp);
CREATE INDEX IF NOT EXISTS log_index_5 ON logs(type, userid, roomid, timestamp);

PRAGMA journal_mode=WAL;
