__author__ = 'Blake VandeMerwe'

import os
import sys
import functools

import simplejson as json
from gevent import monkey; monkey.patch_all()
from bottle import Bottle, run, static_file
from bottle import jinja2_view, jinja2_template as template
from bottle_sqlite import SQLitePlugin

from routes.api import api as pollyApi
import utils

app = Bottle()
cwd = os.getcwd()

config_file = os.path.join(cwd, 'polly.conf')

app.config.load_config(config_file)

conf = lambda x, y: app.config.get(x, y)
view = functools.partial(jinja2_view, template_lookup=[conf('polly.template_dir', './templates')])

check_files = [
    'polly.btsync_path',
    'polly.btsync_conf_path',
    'sqlite.db'
]

if not os.path.exists(config_file):
    raise EnvironmentError('Could not find polly.conf')

for f in check_files:
    if not os.path.exists(conf(f, '')): raise EnvironmentError('Could not find {0}'.format(f))

btsync_conf = json.load(open(conf('polly.btsync_conf_path', ''), 'r+b'))
app.install(SQLitePlugin(dbfile=conf('sqlite.db', ':memory:')))

@app.route('/')
@view('default.html')
def index():
    return {'path': conf('polly.template_dir', None)}

@app.route('/static/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root=os.path.join(cwd, conf('polly.statics_dir', './static')))

if __name__ == '__main__':
    utils.force_btsync_restart(conf)

    # app.mount('/api/', pollyApi)
    # if utils.force_btsync_restart(conf):
    #     run(app,
    #         debug = conf('debug', True),
    #         host = conf('host', 'localhost'),
    #         port = conf('port', 8080),
    #         server = conf('server', 'wsgiref'),
    #         reloader = conf('reloader', conf('debug', True)))
    # else:
    #     sys.exit(1)