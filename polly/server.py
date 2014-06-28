__author__ = 'Blake VandeMerwe'
import os
import sys
import functools
from bottle import Bottle, run, static_file
from bottle import jinja2_view
from bottle_sqlite import SQLitePlugin

app = Bottle()
app.config.load_config(os.path.join(os.getcwd(), 'polly.conf'))
app.install(SQLitePlugin(dbfile=app.config.get('sqlite.db', ':memory:')))

view = functools.partial(jinja2_view, template_lookup=[app.config.get('polly.template_dir', './templates')])

@app.route('/')
@view('default.html')
def index():
    return {'path': app.config.get('polly.template_dir', None)}

@app.route('/static/<path:path>', name='static')
def callback(path):
    return static_file(path, root='static')

run(app,
    debug = app.config.get('debug', True),
    host = app.config.get('host', 'localhost'),
    port = app.config.get('port', 8080),
    reloader = app.config.get('reloader', app.config.get('debug', True)))