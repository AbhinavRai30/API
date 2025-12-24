from pydantic import BaseModel
from datetime import datetime

class ActorBase(BaseModel):
    first_name: str
    last_name: str

class ActorCreate(ActorBase):
    pass

class ActorUpdate(ActorBase):
    pass

class ActorResponse(ActorBase):
    actor_id: int
    last_update: datetime | None

    class Config:
        from_attributes = True
