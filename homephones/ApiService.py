#!/usr/bin/env python
"""Home phones API service."""

import logging

from flask import Flask
from homephones.views.v1.api import apiv1

LOG = logging.getLogger(__name__)

class ApiService(object):

    app = Flask(__name__)
    app.register_blueprint(apiv1)

    def __init__(self, **kwargs):
        pass

    def run(self):
        self.app.run(debug=True)

    @staticmethod
    @app.route("/")
    def index():
        return "Home phones", 200
