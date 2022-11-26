from datetime import datetime

from sqlalchemy import Column, DateTime, Text
from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AgentRecorderEvent(Base):
    __tablename__ = 'agent_recorder_events'
    id = Column(Integer, primary_key=True)
    type = Column(Text)
    message = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f""
