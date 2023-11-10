CREATE TABLE connection_events (
    connection_event_id INTEGER NOT NULL PRIMARY KEY,
    disconnect_time DATETIME NOT NULL,
    reconnect_time DATETIME,
    duration TEXT
);