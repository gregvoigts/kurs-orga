from flask import Flask, render_template
from flask import request
from .dependencies import database
from . import models
from sqlmodel import select

app = Flask(__name__)

db = database.get().__next__()


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/rueckmeldung")
def rueckmeldung():
    db = database.get().__next__()
    token = request.args.get("token")

    if token is None:
        return "Token is missing", 400

    base_url = request.base_url
    url = base_url + "?token=" + token

    stmt = select(models.PersonMeeting).where(
        models.PersonMeeting.token == token)
    person = db.exec(stmt).first()

    if person is None:
        return "Invalid Token", 400

    if not request.args.get("feedback"):
        return render_template("feedback.html", person=person, url=url)

    feedback = request.args.get("feedback")
    person.attended = feedback == "Y"
    db.add(person)
    db.commit()
    db.refresh(person)
    return render_template("feedback.html", complete=True, person=person, url=url)


@app.route("/showPersons")
def showPersons():
    db = database.get().__next__()
    meeting_id = request.args.get("meeting_id")
    stmt = select(models.PersonMeeting, models.Person).join(models.Person).where(models.PersonMeeting.attended ==
                                                                                 True and models.PersonMeeting.meeting_id == meeting_id)
    persons = db.exec(stmt).all()
    return persons[0][1].name
