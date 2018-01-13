from flask import Flask
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/')


@ask.intent('GetSchoolDeadlinesIntent')
def get_school_deadlines(college):
    """Get the admissions deadlines for the provided college."""
    return statement(u'You asked for {}'.format(college))
