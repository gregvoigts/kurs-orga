from typing import Optional
from sqlmodel import Field, SQLModel


class Person(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str


class Meeting(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str


class PersonMeeting(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    person_id: int | None = Field(default=None, foreign_key="person.id")
    meeting_id: int | None = Field(default=None, foreign_key="meeting.id")
    token: Optional[str] = None
    attended: Optional[bool] = None
