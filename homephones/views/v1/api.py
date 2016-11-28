#!/usr/bin/env python
"""Home phones API views v1."""

import logging
import twilio.twiml
import paho.mqtt.client as mqtt
import json
import datetime

from flask import Blueprint, Response, request, url_for
from homephones.config import lookup_number, is_rejected_number, load_config
from homephones.dialhelper import evalute_number

LOG = logging.getLogger(__name__)


api = Blueprint('apiv1', __name__, url_prefix='/v1')


def mqtt_log_call(direction, category, from_number, to_number):
    cfg = load_config()
    mqtt_cfg = cfg["mqtt"]
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(mqtt_cfg["username"], mqtt_cfg["password"])
    mqtt_client.connect(mqtt_cfg["broker"], mqtt_cfg["port"], 60)
    topic = "%s/%s/%s" % (mqtt_cfg["topic_prefix"], direction, category)

    from_callerid = lookup_number(number=from_number)
    if from_callerid is None:
        from_callerid = ""
        from_display = from_number
    else:
        from_display = from_callerid

    to_callerid = lookup_number(number=to_number)
    if to_callerid is None:
        to_callerid = ""
        to_display = to_number
    else:
        to_display = to_callerid

    payload = {
        "from_number": from_number,
        "from_callerid": from_callerid,
        "from_display": from_display,
        "to_number": to_number,
        "to_callerid": to_callerid,
        "to_display": to_display,
        "when": datetime.datetime.now().strftime('%a %H:%M')
    }
    mqtt_client.publish(topic=topic, payload=json.dumps(payload))
    return


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
    called = str(request.form["To"])
    caller = str(request.form["Caller"]).replace("client:", "")
    response = twilio.twiml.Response()
    mqtt_log_call(direction="incoming", category="prefilter", from_number=caller, to_number=called)
    # should we reject it? spam?
    reject = is_rejected_number(number=caller)
    if reject is not None:
        mqtt_log_call(direction="incoming", category="rejected", from_number=caller, to_number=called)
        response.reject()
        return twiml(response)

    response.say("Thank you for calling Claire and Nat, please hold.", voice="alice", language="en-GB")

    # lookup caller id
    callerid = lookup_number(number=caller)
    if callerid is None:
        callerid = caller
    response.dial(callerId=callerid, action=url_for('apiv1.from_external_dial_action', _external=True), method="POST").sip("cordlessphone1@esgob.sip.us1.twilio.com")
    mqtt_log_call(direction="incoming", category="ringing", from_number=caller, to_number=called)
    return twiml(response)


@api.route("/from_external_dial_action/", methods=['POST'])
def from_external_dial_action():
    response = twilio.twiml.Response()
    return twiml(response)


@api.route("/from_internal/", methods=['POST'])
def from_internal():
    called = str(request.form["Called"])
    number = called.split("@")[0].split("sip:")[1]
    (fullnumber, describednumber) = parse_dialed_number(number=number)
    mqtt_log_call(direction="outgoing", category="dialing", from_number="+441437766027", to_number=fullnumber)
    response = twilio.twiml.Response()
    response.say("Calling %s" % (describednumber), voice="alice", language="en-GB")
    response.dial(number=fullnumber, callerId="+441437766027", action=url_for('apiv1.from_internal_dial_action', _external=True))
    return twiml(response)


@api.route("/from_internal_dial_action/", methods=['POST'])
def from_internal_dial_action():
    response = twilio.twiml.Response()
    return twiml(response)


@api.route("/status_callback/", methods=['POST'])
def status_callback():
    response = twilio.twiml.Response()
    return twiml(response)
