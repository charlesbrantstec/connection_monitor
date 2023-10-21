from sqlalchemy import Column, Integer, String, DateTime, Sequence
import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ConnectionEvent(Base):
    __tablename__ = 'connection_events'
    
    connection_event_id = Column(Integer, Sequence('connection_event_id_seq'), primary_key=True)
    disconnect_time = Column(DateTime, default=datetime.datetime.now, nullable=False) # Defaulting this
    reconnect_time = Column(DateTime)
    duration = Column(String)
