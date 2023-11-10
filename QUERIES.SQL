--SQLite
DROP TABLE IF EXISTS connection_monitor.connection_events;

INSERT INTO connection_events (disconnect_time, reconnect_time, duration)
VALUES (datetime('now'), datetime('now', '+1 minute') , '00:01');

DELETE FROM connection_events WHERE connection_event_id = 1;
UPDATE connection_events SET  connection_event_id = 1000 where connection_event_id = 2;

DELETE FROM connection_events WHERE connection_event_id != 1000;

DELETE FROM connection_events;

DELETE FROM connection_events WHERE connection_event_id != 1;
update connection_events set connection_event_id = 999 where connection_event_id = 1;
DELETE FROM connection_events WHERE connection_event_id = 999;
UPDATE connection_events SET reconnect_time = NULL WHERE connection_event_id = 1029;
DELETE FROM CONNECTION_EVENTS WHERE connection_event_id = 1030;
