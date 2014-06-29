__author__ = 'Blake VandeMerwe'

import functools

import os
import simplejson as json

from gevent import monkey
monkey.patch_all()

import gevent
from socketio.server import SocketIOServer
from socketio import socketio_manage

from bottle import Bottle, static_file
from bottle import jinja2_view
from bottle import request
from bottle_sqlite import SQLitePlugin

from routes.api import api as pollyApi
from btsync import BtsyncApi
from pollyo import StatusNamespace
import utils

app = Bottle()
cwd = os.getcwd()

config_file = os.path.join(cwd, 'polly.conf')

app.config.load_config(config_file)

conf = utils.conf(app)
view = functools.partial(jinja2_view, template_lookup=[conf('polly.template_dir', './templates')])

check_files = [
    'polly.btsync_path',
    'polly.btsync_conf_path',
    'polly.template_dir', 'polly.statics_dir',
    'sqlite.db'
]

if not os.path.exists(config_file):
    raise EnvironmentError('Could not find polly.conf')

for f in check_files:
    if not os.path.exists(conf(f, '')): raise EnvironmentError('Could not find {0}: {1}'.format(f, conf(f, '')))

btsync_conf = json.load(open(conf('polly.btsync_conf_path', ''), 'r+b'))
btsync = BtsyncApi(conf('polly.btsync_conf_path', ''))

app.debug = conf('debug', False)
app.install(SQLitePlugin(dbfile=conf('sqlite.db', ':memory:')))

@app.route('/')
@view('default.html')
def index():
    return {}

@app.route('/static/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root=os.path.join(cwd, conf('polly.statics_dir', './static')))

@app.route('/socket.io/<arg:path>', method=['OPTIONS', 'GET'])
def socketio(*args, **kwargs):
    path = request.environ['PATH_INFO'].strip('/')
    if path.startswith('socket.io'):
        socketio_manage(request.environ, {'/status': StatusNamespace}, request)
    else:
        return {'error': 'socket-io endpoint not found'}

if __name__ == '__main__':
    app.mount('/api/', pollyApi)

    http_server = SocketIOServer(
        (conf('host', 'localhost'), int(conf('port', 8085))), app, resource='socket.io')

    gevent.joinall([
        gevent.spawn(http_server.serve_forever)
    ])