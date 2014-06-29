__author__ = 'Blake VandeMerwe'

import os
from bottle import Bottle
from btsync import BtsyncApi
from utils import conf

# define new api app
api = Bottle()
# get the cwd and find the configuration file used in server.py
cwd = os.getcwd()
config_file = os.path.join(cwd, 'polly.conf')
# load the same config values into this api, as it's just an extension
api.config.load_config(config_file)
# prime utils.conf with the current app we're using
conf = conf(api)
# get the btsync configuration path
btsync = BtsyncApi(conf('polly.btsync_conf_path'))

@api.route('/btsync_stats')
def api_get_dirs():
    return {
        'btsync': {
            'version': btsync.get_version()['version'],
            'speed': btsync.get_speed(),
            'os': btsync.get_os()['os']
        }
    }
