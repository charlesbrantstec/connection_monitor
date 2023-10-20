import sqlite3

conn = sqlite3.connect("connection_monitor.db")
cursor = conn.cursor()

cursor.execute('''
DROP TABLE IF EXISTS connection_events;
               ''')
conn.commit()


cursor.execute('''
DROP TABLE IF EXISTS connection_events;
CREATE TABLE connection_events (
    connection_event_id INT NOT NULL AUTO INCREMENT,
    disconnect_time DATETIME NOT NULL,
    reconnect_time DATETIME,
    duration VARCHAR
) AUTO_INCREMENT = 1000;
''')

conn.commit()
conn.close()
