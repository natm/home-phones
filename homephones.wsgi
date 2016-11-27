import sys
sys.path.insert(0, '/var/www/phones/')

from homephones.ApiService import ApiService

svc = ApiService()
application = svc.app
