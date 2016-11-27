import os
import sys
sys.path.insert(0, '/var/www/phones/')

from homephones.ApiService import ApiService



def application(environ, start_response):
    svc = ApiService()
    return svc.app(environ, start_response)
