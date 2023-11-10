import time
import requests
from Model.ConnectionEvent import ConnectionEvent
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime

# Configuration
CHECK_INTERVAL = 10  # seconds
LOG_FILE = "connection_log.txt"
TEST_URL = "https://www.google.com"

def setup_session():
    DATABASE_URL = "sqlite:///Database/connection_monitor.db"
    engine = create_engine(DATABASE_URL)
    print("connected to database")
    return sessionmaker(bind=engine)

def has_internet(): 
    # Check if we can make a successful request to google
    try:
        response = requests.get(TEST_URL, timeout=5) # 5 second timeout
        return True if response.status_code == 200 else False
    except (requests.ConnectionError, requests.Timeout, requests.RequestException):
        return False

def create_disconnect_rec(session):
    # Create the intial record with just the disconnect datetime
    new_event = ConnectionEvent()  
    session.add(new_event)
    session.commit()

def update_reconnect_time(session):
    # Fetch the most recent ConnectionEvent based on the disconnect_time
    event = session.query(ConnectionEvent).order_by(ConnectionEvent.disconnect_time.desc()).first()

    if event:  # if a record was found
        event.reconnect_time = datetime.datetime.now()
        duration = event.reconnect_time - event.disconnect_time
        event.duration = str(duration)
        session.commit()
    
def log_event(event_msg):
    # log disconnect/reconnect with timetstamps to log file
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as log:
        log.write(f"{timestamp} - {event_msg}\n")

def delete_stuck_record(session):
    # If the application crashes check if the last record is stuck with a null reconnect time
    # A power outage or a nuclear bomb is not an ISP issue
    while True: # Look for multiple stuck records
        event = session.query(ConnectionEvent).order_by(ConnectionEvent.disconnect_time.desc()).first()
        if event.reconnect_time is None:
            session.delete(event)
            session.commit()

    

def main():
    Session = setup_session()
    session = Session()
    last_status = has_internet() # state change in this boolean drives disonnect creation and subsequent reconnection update

    if not last_status:            
        log_event("Internet disconnected")
        create_disconnect_rec(session) # Create new connection_events record

    while True: # This will loop continuously until the program is terminated or an unhandled exception occurs
        current_status = has_internet()
        
        # if last_status == current_status:
        #     delete_stuck_record(session)
             
        if current_status != last_status: # If there was a change in the connection status
            if current_status:

                log_event("Internet reconnected") # Log event to log file
                # create_disconnect_rec(session) # Create new connection_events record 
                update_reconnect_time(session)
            else:

                log_event("Internet disconnected")
                # update_reconnect_time(session)
                create_disconnect_rec(session) # Create new connection_events record 
        
        last_status = current_status
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
