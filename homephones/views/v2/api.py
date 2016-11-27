#!/usr/bin/env python
"""Home phones API views v1."""

import logging
import twilio.twiml

from flask import Blueprint, Flask, redirect, url_for, Response, request
from homephones.dialhelper import evalute_number

LOG = logging.getLogger(__name__)


api = Blueprint('apiv2', __name__, url_prefix='/v2')

def parse_dialed_number(number):
    fullnumber = evalute_number(dialed=number)
    describednumber = "Test"
    return (fullnumber, describednumber)

def twiml(resp):
    resp = Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp

@api.route("/")
def index():
    return "Home phones v2", 200

@api.route("/from_external/", methods=['POST'])
def from_external():
    caller = str(request.form["Caller"]).replace("client:", "")
    #response = twilio.twiml.Response()
    #response.say("Thank you for calling Claire and Nat, please hold.", voice="alice", language="en-GB")
    #response.dial(callerId=caller).sip("officephone1@esgob.sip.us1.twilio.com").sip("cordlessphone1@esgob.sip.us1.twilio.com")
    #return twiml(response)

    x = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Say language="en-GB" voice="alice">Please hold</Say>
<Dial callerId="TEST" action="https://phones.gorras.hw.esgob.com/v1/call_action/">
    <Sip>officephone1@esgob.sip.us1.twilio.com</Sip>
</Dial>
<Dial callerId="TEST" action="https://phones.gorras.hw.esgob.com/v1/call_action/">
    <Sip>natimac1@esgob.sip.us1.twilio.com</Sip>
</Dial>
</Response>"""
    #resp = Response(x)
    #resp.headers['Content-Type'] = 'text/xml'
    #return resp
    response = twilio.twiml.Response()
    response.say("please hold")
    response.enqueue(name="inbound")
    return twiml(response)
    #response.say("please hold.", voice="alice", language="en-GB")
    #response.enqueue(callerId=caller).sip("officephone1@esgob.sip.us1.twilio.com").sip("cordlessphone1@esgob.sip.us1.twilio.com")
    #return twiml(response)

@api.route("/from_internal/", methods=['POST'])
def from_internal():
    called = str(request.form["Called"])
    number = called.split("@")[0].split("sip:")[1]
    (fullnumber, describednumber) = parse_dialed_number(number=number)
    response = twilio.twiml.Response()
    response.say("Calling %s" % (describednumber), voice="alice", language="en-GB")
    response.dial(number=fullnumber, callerId="+441437766027")
    return twiml(response)

@api.route("/call_action/", methods=['POST'])
def call_action():
    resp = Response("""<?xml version="1.0" encoding="UTF-8"?>
<Response>
</Response>""")
    resp.headers['Content-Type'] = 'text/xml'
    return resp

@api.route("/status_callback/", methods=['POST'])
def status_callback():
    return ""
