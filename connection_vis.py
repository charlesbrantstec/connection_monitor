import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Set up the database connection
DATABASE_URL = "sqlite:///Database/connection_monitor.db"  # replace with your database URL
engine = create_engine(DATABASE_URL)

# Load data from connection_events table into a pandas DataFrame
df = pd.read_sql("SELECT * FROM connection_events", engine)

# Convert disconnect_time into datetime type
df['disconnect_time'] = pd.to_datetime(df['disconnect_time'])

# Resample data by, say, hours and count the number of disconnects in each hour
disconnect_counts = df.resample('H', on='disconnect_time').size()

# Plot the line graph
plt.figure(figsize=(15, 6))
disconnect_counts.plot()

plt.title('Number of Disconnections Over Time')
plt.xlabel('Time')
plt.ylabel('Number of Disconnects')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()