#!/usr/bin/env python
"""Home phones API service."""

import logging

from flask import Flask, redirect

LOG = logging.getLogger(__name__)


class ApiService(object):

    app = Flask(__name__)

    def __init__(self, **kwargs):
        pass

    def run(self):
        self.app.run(debug=True)
