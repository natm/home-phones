#!/usr/bin/env python
"""Home phones API views v1."""

import logging
import twilio.twiml

from flask import Blueprint, Response, request
from homephones.config import lookup_number, is_rejected_number
from homephones.dialhelper import evalute_number

LOG = logging.getLogger(__name__)


api = Blueprint('apiv1', __name__, url_prefix='/v1')


def parse_dialed_number(number):
    fullnumber = evalute_number(dialed=number)
    describednumber = lookup_number(number=fullnumber)
    if describednumber is None:
        describednumber = fullnumber
    return (fullnumber, describednumber)


def twiml(resp):
    resp = Response(str(resp))
    resp.headers['Content-Type'] = 'text/xml'
    return resp


@api.route("/")
def index():
    return "Home phones v1", 200


@api.route("/from_external/", methods=['POST'])
def from_external():
    caller = str(request.form["Caller"]).replace("client:", "")
    response = twilio.twiml.Response()

    # should we reject it? spam?
    reject = is_rejected_number(number=caller)
    if reject is not None:
        response.reject()
        return twiml(response)

    response.say("Thank you for calling Claire and Nat, please hold.", voice="alice", language="en-GB")
    # lookup caller id
    callerid = lookup_number(number=caller)
    if callerid is None:
        callerid = caller
    response.dial(callerId=callerid).sip("cordlessphone1@esgob.sip.us1.twilio.com")
    return twiml(response)


@api.route("/from_internal/", methods=['POST'])
def from_internal():
    called = str(request.form["Called"])
    number = called.split("@")[0].split("sip:")[1]
    (fullnumber, describednumber) = parse_dialed_number(number=number)
    response = twilio.twiml.Response()
    response.say("Calling %s" % (describednumber), voice="alice", language="en-GB")
    response.dial(number=fullnumber, callerId="+441437766027")
    return twiml(response)


@api.route("/status_callback/", methods=['POST'])
def status_callback():
    return ""
