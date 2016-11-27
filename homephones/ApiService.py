#!/usr/bin/env python
"""Home phones API service."""

import logging

from flask import Flask
from homephones.views.v1.api import api as apiv1
from homephones.views.v2.api import api as apiv2

LOG = logging.getLogger(__name__)

class ApiService(object):

    app = Flask(__name__)
    app.register_blueprint(apiv1)
    app.register_blueprint(apiv2)

    def __init__(self, **kwargs):
        pass

    def run(self):
        self.app.run(debug=True)

    @staticmethod
    @app.route("/")
    def index():
        return "Home phones", 200
