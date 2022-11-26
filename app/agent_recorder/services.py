from typing import List

from sqlalchemy.orm import Session

from app.agent_recorder.models import AgentRecorderEvent
from app.agent_recorder.serializers import AgentRecorderEventListSerializer
from app.main.config import engine


class AgentRecorderEventService:
    def handle_event(self, events: List[AgentRecorderEventListSerializer]) -> None:
        events_to_save = []

        for event in events:
            events_to_save.append(
                AgentRecorderEvent(
                    type=event.type,
                    message=event.message,
                )
            )

        with Session(engine) as session:
            session.add_all(events_to_save)
            session.commit()
