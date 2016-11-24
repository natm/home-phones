# Home phones

Call routing using [Twilio](http://www.twilio.com). We have a handful of incoming UK numbers with them, mostly ported in from elsewhere (as they work out cheaper than many UK VOIP providers).

Multiple SIP handsets in the house are registered to a SIP domain hosted in our Twilio account.

This Flask application handles all our call routing:

* Inbound from PSTN to handsets
* Between handsets
* Output from handsets to PSTN

Each event generates an MQTT message which is publish on the message bus, examples:

```

```

![Workflow](https://raw.github.com/natm/home-phones/master/docs/workflow.png)

## Historical

2002

* BT PSTN line (same as ADSL)

2010

* Moved house, kept same number

2011

* Bought some AQL numbers
* Ported existing house number to AQL
* Inbound + outbound calls via an AQL SIP trunk
* Inbound via AQL, outbound via local phone

2016

* Ported 3 numbers from AQL to Twilio, £2.40/number/month vs $1.00/number/month
* Moved house
* Asterisk VM running on colo in London
* Three SIP devices at home

2017

* Twilio SIP registration announced
* Wrote this Flask call routing endpoint
* Turned off Asterisk VM

## Development

```
clone
cd
venv
source
pip
pip
tests
./run.py
```

## License

MIT
