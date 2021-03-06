import os

from flask import Flask, got_request_exception, request
from flask_ask import Ask, question, statement
import rollbar
import rollbar.contrib.flask

app = Flask(__name__)
ask = Ask(app, '/')

# Add protection from other skills.
skill_id = 'amzn1.ask.skill.d4d0d1bc-2c5f-4fff-96da-dc2cc927a8ef'
app.config['ASK_APPLICATION_ID'] = skill_id

DEADLINES = [
    'For Harvard University, the regular decision deadline is January 1, 2018.',
    'For the University of Virginia, the regular decision deadline is January 1, 2018.',
    'For Yale University, the regular decision deadline is January 2, 2018.',
]


def report_exception(app, exception):
    rollbar.report_exc_info(request=request)
    # Wait or else Rollbar won't finish before the Lambda goes away.
    rollbar.wait()


@app.before_first_request
def init_rollbar():
    """Initialize Rollbar."""
    rollbar.init(
        os.environ['ROLLBAR_ACCESS_TOKEN'],
        os.environ['STAGE'],
        # Flask already sets up logging.
        allow_logging_basic_config=False)

    # Send exceptions from `app` to Rollbar, using Flask's signal system.
    got_request_exception.connect(report_exception, app)


@ask.launch
def launch():
    """Ask a greeting question when launched."""
    school_question = 'what school would you like deadlines for?'
    greeting = 'Hello from College Conductor, {}'.format(school_question)
    response = question(greeting).reprompt(school_question.capitalize())
    return response.simple_card('College Admissions Deadlines', greeting)


@ask.intent('GetSchoolDeadlinesIntent')
def get_school_deadlines(college):
    """Get the admissions deadlines for the provided college."""
    if college:
        college = college.lower()
        for deadline in DEADLINES:
            if college in deadline.lower():
                return statement(deadline)
    return statement(
        'Sorry, we are still collecting data for that school. '
        'Please try again in a couple of days.'
    )


@ask.session_ended
def session_ended():
    """Cleanly close the session."""
    return '{}', 200


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement('Goodbye')


@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = 'Ask us what school you would like deadlines for'
    school_question = 'what school would you like deadlines for?'
    return question(help_text).reprompt(school_question)


@ask.intent('AMAZON.StopIntent')
def stop():
    return statement('Goodbye')


if __name__ == '__main__':
    app.run(debug=True)
