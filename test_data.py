import time
import requests
from Model.ConnectionEvent import ConnectionEvent
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime

# Configuration
CHECK_INTERVAL = 10  # seconds
LOG_FILE = "connection_log.txt"

with open('connection_log.txt', 'r', encoding='utf-8') as file:
    LOG = file.readlines()

def setup_session():
    DATABASE_URL = "sqlite:///Database/connection_monitor.db"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)  
    return Session

def domains_objs_from_log():
    i = 0
    records = []
    record = []
    for line in LOG:
        i += 1
        if ( i % 2 != 0):
            record = []
            record.append(line[0:19])
        elif ( i % 2 == 0):
            record.append(line[0:19])
            records.append(record)
    print(records)
    
    for record in records:
        record[0] = datetime.datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S')
        record[1] = datetime.datetime.strptime(record[1], '%Y-%m-%d %H:%M:%S')

    return records

def main():
    Session = setup_session()
    with Session() as session:
        for record in domains_objs_from_log():
            new_event = ConnectionEvent()
            new_event.disconnect_time = record[0]
            new_event.reconnect_time = record[1]
            duration = record[1] - record[0]
            new_event.duration = str(duration)
            session.add(new_event)
        session.commit()

if __name__ == "__main__":
    main()
