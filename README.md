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
