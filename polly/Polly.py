import os
import datetime
import simplejson as json
import functools

from bottle import Bottle, static_file
from bottle import jinja2_view
from bottle_sqlite import SQLitePlugin

from btSync import BtsyncApi
import Utils

from generate_config import generate

configs = ['polly.conf', 'btsync.conf']


for config in configs: # if the configuration files don't exist
    if not os.path.exists(os.path.join(os.getcwd(), config)):
        generate(None, True) # make them
        break

config = Utils.convert(json.load(open(os.path.join(os.getcwd(), 'polly.conf'), 'r+b')))

def build(*args, **kwargs):
    app = Bottle()
    config = kwargs.get('config', {})
    bottle_config = config.get('default', {})
    polly_config = config.get('polly', {})
    sqlite_config = config.get('sqlite', {})
    app.config.load_dict(config)
    app.debug = bottle_config.get('debug', False)
    app.config['started'] = datetime.datetime.now()
    return app

app = build(config = config)
view = functools.partial(jinja2_view, template_lookup=[app.config['polly.template_dir']])

@app.route('/')
@view('index.html')
def index(): return {}

@app.route('/info')
def info():
    return {
        'started': app.config['started'].strftime('%m-%d %H:%M:%S')}

@app.route('/static/<filename:path>', name='static')
def serve_static(filename):
    return static_file(filename, root = app.config['polly.statics_dir'])

if __name__ == '__main__':
    app.run(host = app.config['default.host'],
            port = app.config['default.port'],
            reloader = app.config['default.reloader'],
            server = app.config['default.server'])