from flask import Flask
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/')

# Add protection from other skills.
skill_id = 'amzn1.ask.skill.d4d0d1bc-2c5f-4fff-96da-dc2cc927a8ef'
app.config['ASK_APPLICATION_ID'] = skill_id


@ask.intent('GetSchoolDeadlinesIntent')
def get_school_deadlines(college):
    """Get the admissions deadlines for the provided college."""
    return statement(u'You asked for {}'.format(college))
