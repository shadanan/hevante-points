"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

import requests

DOC_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSfg9heoTc9KDA9mjTZWpuvtRqXSjoK_Q0wSKIkPyAxUvAtLog/formResponse'


Tal = 'Tal'
Shad = 'Shad'
Rhyan = 'Rhyan'
Rahul = 'Rahul'
Julia = 'Julia'
Emily = 'Emily'

name_map = {
    'tal': Tal,
    'tall': Tal,
    'shad': Shad,
    'ryan': Rhyan,
    'rahul': Rahul,
    'emily': Emily,
    'julia': Julia
}

def remap_name(name):
    return name_map.get(name.lower(), None)


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome to Hevante Points skill."
    speech_output = (
        "Welcome to the Hevahnty Points skill. You can say, "
        "Alexa, ask Hevahnty to send Emily 5 points from Julia for being awesome.")
    reprompt_text = (
        "I'm sorry, I didn't understand. You can say, "
        "Alexa, ask Hevahnty to send Tal 5 points from Shad for helping a lot.")

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def send_hevante_points(intent, session):
    session['card_title'] = intent['name']

    session['points'] = intent['slots']['Points'].get('value')
    session['dest'] = remap_name(intent['slots']['Dest'].get('value')
    session['src'] = remap_name(intent['slots']['Source'].get('value')
    session['reason'] = intent['slots']['Reason'].get('value')

    prompt_for_args(session)
    
def get_points(intent, session):
    session['card_title'] = intent['name']
    session['points'] = intent['slots']['Points']['value']

    return prompt_for_args(session)

def get_name(intent, session):
    session['card_title'] = intent['name']
    
    if session['prompt'] == 'dest':
        session['dest'] = remap_name(intent['slots']['Dest']['value'])
    else:
        session['src'] = remap_name(intent['slots']['Source']['value'])

    return prompt_for_args(session)
       
def get_reason(intent, session):
    session['card_title'] = intent['name']
    session['reason'] = intent['slots']['Reason']['value']

    return prompt_for_args(session)

def prompt_for_args(session):
    print("Session: %s" % session) 
    should_end_session = False
    points = session.get('points')
    dest = session.get('dest')
    src = session.get('src')
    reason = session.get('reason')

    if points is None:
        session['prompt'] = 'points'
        speech_output = "How many Hevahnty points should I send?"
    elif dest is None:
        session['prompt'] = 'dest'
        speech_output = "Who should I send %s Hevahnty points to?" % points
    elif src is None:
        session['prompt'] = 'src'
        speech_output = "Who am I sending %s Hevahnty points from?" % points
    elif reason is None:
        session['prompt'] = 'reason']
        speech_output = "Why am I sending %s %s points?" % (dest, points)
    else:
        should_end_session = True
        result = do_post(src, dest, points, reason)
        if result:
            speech_output = "Okay. Sent %s %s points from %s for %s" % (dest, points, src, reason)
        else:
            speech_output = "Sorry, I could not send %s %s points from %s for %s" % (dest, points, src, reason)

    reprompt_text = "Sorry, I didn't catch that." + speech_output
    return build_response(session, build_speechlet_response(
        session['card_title'], speech_output, reprompt_text, should_end_session))

def do_post(src, dest, points, reason):
    form_data = {
        'entry.354337782': src,
        'entry.729579027': dest,
        'entry.267707373': points,
        'entry.729332833': reason,
        'draftResponse': [],
        'pageHistory': 0
    }

    print('Post Data: %s' % str(form_data))
    response = requests.post(DOC_URL, data=form_data)

    return response.status_code == 200

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using the Hevahnty Points skill!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "SendHevantePoints":
        return send_hevante_points(intent, session)
    elif intent_name == "GetPoints":
        return get_points(intent, session)
    elif intent_name == "GetName":
        return get_name(intent, session)
    elif intent_name == "GetReason":
        return get_reason(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent: %s" % intent_name)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

