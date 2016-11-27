import os
import sys
sys.path.insert(0, '/var/www/phones/')


def application(environ, start_response):
    for key in ['PHONES_CONFIG']:
        os.environ[key] = environ.get(key, '')
    from homephones.ApiService import ApiService
    svc = ApiService()
    return svc.app(environ, start_response)
