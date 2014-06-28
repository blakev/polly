__author__ = 'Blake VandeMerwe'
import os
import functools
from gevent import monkey; monkey.patch_all()
import time
from bottle import Bottle, run, static_file
from bottle import jinja2_view
from bottle_sqlite import SQLitePlugin

config_file = os.path.join(os.getcwd(), 'polly.conf')

if not os.path.exists(config_file):
    raise ImportError('Could not find polly.conf file!')

app = Bottle()
app.config.load_config(config_file)

conf = lambda x, y: app.config.get(x, y)
view = functools.partial(jinja2_view, template_lookup=[conf('polly.template_dir', './templates')])

app.install(SQLitePlugin(dbfile=conf('sqlite.db', ':memory:')))

@app.route('/')
@view('default.html')
def index():
    return {'path': conf('polly.template_dir', None)}

@app.get('/api/dirs')
def callback():
    for root, dirs, files in os.walk(r'F:\btsync\projects\polly', followlinks = conf('polly.allow_symlinks')):
        for name in files:
            yield name + '<br>'

@app.route('/static/<path:path>', name='static')
def callback(path):
    return static_file(path, root='static')

run(app,
    debug = conf('debug', True),
    host = conf('host', 'localhost'),
    port = conf('port', 8080),
    server = conf('server', 'wsgiref'),
    reloader = conf('reloader', conf('debug', True)))