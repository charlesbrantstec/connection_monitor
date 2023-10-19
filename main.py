import time
import requests

# Configuration
CHECK_INTERVAL = 10  # seconds
LOG_FILE = "connection_log.txt"
TEST_URL = "https://www.google.com"

def has_internet(): # check if we can make a successful request to google
    try:
        response = requests.get(TEST_URL, timeout=5) # 5 second timeout
        return True if response.status_code == 200 else False
    except (requests.ConnectionError, requests.Timeout, requests.RequestException):
        return False

def log_event(event_msg):
    # log disconnect/reconnect with timetstamps to log file
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as log:
        log.write(f"{timestamp} - {event_msg}\n")

def main():
    last_status = has_internet()

    while True: # This will loop continuously until the program is terminated or an unhandled exception occurs
        current_status = has_internet()
        
        # If there was a change in the connection status
        if current_status != last_status:
            if current_status:
                log_event("Internet reconnected")
            else:
                log_event("Internet disconnected")
        
        last_status = current_status
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
