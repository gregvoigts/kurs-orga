from sqlmodel import SQLModel, create_engine
from sqlmodel import Session
from .. import models


sqlite_file_name = "../database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

# Clear the database TODO: Remove this line in production
SQLModel.metadata.drop_all(engine)


SQLModel.metadata.create_all(engine)

db = Session(engine, autoflush=False, autocommit=False)

# Create sample data for Person class
person1 = models.Person(name="John Doe", email="john.doe@example.com")
person2 = models.Person(name="Jane Smith", email="jane.smith@example.com")

# Create sample data for Meeting class
meeting1 = models.Meeting(title="Project Kickoff",
                          description="Introduction to the project")
meeting2 = models.Meeting(title="Weekly Standup",
                          description="Status update meeting")

demo_data = [person1, person2, meeting1, meeting2]

for data in demo_data:
    db.add(data)
    db.commit()
    db.refresh(data)

# Create sample data for PersonMeeting class
person_meeting1 = models.PersonMeeting(
    person_id=person1.id, meeting_id=meeting1.id, token="abc123")
person_meeting2 = models.PersonMeeting(
    person_id=person2.id, meeting_id=meeting1.id, token="def456")
person_meeting3 = models.PersonMeeting(
    person_id=person1.id, meeting_id=meeting2.id, token="ghi789")
person_meeting4 = models.PersonMeeting(
    person_id=person2.id, meeting_id=meeting2.id, token="jkl012")

demo_data = [person_meeting1, person_meeting2,
             person_meeting3, person_meeting4]

db.add_all(demo_data)
db.commit()

db.close()


def get() -> Session:
    """ create new database session """
    # Make Instance from SessionManager (create Session)
    db = Session(engine, autoflush=False, autocommit=False)
    try:
        yield db  # return db-session
    finally:
        db.close()
