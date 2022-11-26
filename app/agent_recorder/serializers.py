from typing import Optional, List

import pydantic
from pydantic import Field


class MessageAgent(pydantic.BaseModel):
    id: Optional[int] = Field(...)


class AgentRecorderEvent(pydantic.BaseModel):
    type: str
    message: Optional[dict]


class AgentRecorderEventListSerializer(pydantic.BaseModel):
    __root__: List[AgentRecorderEvent]
