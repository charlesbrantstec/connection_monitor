--SQLite
DROP TABLE IF EXISTS connection_events;
CREATE TABLE connection_events (
    connection_event_id INT NOT NULL PRIMARY KEY,
    disconnect_time DATETIME NOT NULL,
    reconnect_time DATETIME,
    duration TEXT
);