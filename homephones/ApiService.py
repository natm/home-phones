#!/usr/bin/env python
"""Home phones API service."""

import logging
import twilio.twiml

from flask import Flask, redirect, url_for, Response, request


LOG = logging.getLogger(__name__)

def parse_dialed_number(number):
    fullnumber = "+447531750292"
    describednumber = "Test"
    return (fullnumber, describednumber)

def twiml(resp):
    resp = Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp

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
        caller = str(request.form["Caller"]).replace("client:", "")
        response = twilio.twiml.Response()
        response.say("Thank you for calling Claire and Nat, please hold.", voice="alice", language="en-GB")
        response.dial(callerId=caller).sip("officephone1@esgob.sip.us1.twilio.com")
        return twiml(response)

    @staticmethod
    @app.route("/v1/from_internal/", methods=['POST'])
    def from_internal():
        called = str(request.form["Called"])
        number = called.split("@")[0].split("sip:")[1]
        (fullnumber, describednumber) = parse_dialed_number(number=number)
        response = twilio.twiml.Response()
        response.say("Calling %s" % (describednumber), voice="alice", language="en-GB")
        response.dial(number=fullnumber, callerId="+441437766027")
        return twiml(response)
