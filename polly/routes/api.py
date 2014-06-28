__author__ = 'Blake VandeMerwe'

from bottle import Bottle

api = Bottle()

@api.route('/') # supplies api commands
def api_listing():
    return {'.'.join(x.rule.split('/')):x.rule for x in api.routes}

@api.route('/get_dirs')
def api_get_dirs():
    return 'directories'
