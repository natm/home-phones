#!/usr/bin/env python
"""Home phones API service."""

import logging
import twilio.twiml

from flask import Flask, redirect, url_for, Response, request


LOG = logging.getLogger(__name__)

def twiml(resp):
    resp = Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp

def _give_instructions(response):
    response.say("To get to your extraction point, get on your bike and go down " +
                 "the street. Then Left down an alley. Avoid the police cars. Turn left " +
                 "into an unfinished housing development. Fly over the roadblock. Go " +
                 "passed the moon. Soon after you will see your mother ship.",
                 voice="alice", language="en-GB")

    response.say("Thank you for calling the ET Phone Home Service - the " +
                 "adventurous alien's first choice in intergalactic travel")

    response.hangup()
    return response

def _list_planets(response):
    with response.gather(numDigits=1, action=url_for('planets'), method="POST") as g:
        g.say("To call the planet Broh doe As O G, press 2. To call the planet " +
              "DuhGo bah, press 3. To call an oober asteroid to your location, press 4. To " +
              "go back to the main menu, press the star key ",
              voice="alice", language="en-GB", loop=3)

class ApiService(object):

    app = Flask(__name__)

    def __init__(self, **kwargs):
        pass

    def run(self):
        self.app.run(debug=True)

    @staticmethod
    @app.route("/")
    def index():
        return "Home phones", 200

    @staticmethod
    @app.route("/v1/from_external/", methods=['POST'])
    def from_external():
        response = twilio.twiml.Response()
        with response.gather(numDigits=1, action=url_for('menu'), method="POST") as g:
            g.play(url="http://howtodocs.s3.amazonaws.com/et-phone.mp3", loop=3)
        return twiml(response)

    @staticmethod
    @app.route('/ivr/menu', methods=['POST'])
    def menu():
        selected_option = request.form['Digits']
        option_actions = {'1': _give_instructions,
                          '2': _list_planets}

        if option_actions.has_key(selected_option):
            response = twilio.twiml.Response()
            option_actions[selected_option](response)
            return twiml(response)

        return _redirect_welcome()

    @staticmethod
    @app.route('/ivr/planets', methods=['POST'])
    def planets():
        selected_option = request.form['Digits']
        option_actions = {'2': "+12024173378",
                          '3': "+12027336386",
                          "4": "+12027336637"}

        if option_actions.has_key(selected_option):
            response = twilio.twiml.Response()
            response.dial(option_actions[selected_option])
            return twiml(response)

        return _redirect_welcome()


    # private methods
