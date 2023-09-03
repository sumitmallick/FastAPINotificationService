from typing import Optional
from pydantic import BaseModel, validator


class Subscription(BaseModel):
    id: Optional[int] = None
    description: Optional[str] = None
    app_name: str
    event: str = '*'
    callback_url: str

    @validator('event')
    def event_must_not_empty(cls, v):
        if not v:
            raise ValueError('Event must not be empty')
        return v

    class Config:
        orm_mode = True


class Notification(BaseModel):
    app_name: str
    event: str
    payload: dict = {}
