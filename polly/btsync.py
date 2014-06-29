__author__ = 'Blake VandeMerwe'

import os

import requests
import simplejson as json

immutable_dict = frozenset(dict().items())

default_response = {
    'error': {
        'msg': 'Could not connect to btsync'
    }
}

class BtsyncApi(object):
    def __init__(self, btsync_conf = None, **kwargs):
        if not os.path.exists(btsync_conf) or btsync_conf is None:
            if kwargs:
                self.config = kwargs
            else:
                self.config = {}
        else:
            self.config = json.load(open(btsync_conf, 'r+b'))
        webui = self.config.get('webui', {})
        self.address, self.port = webui.get('listen', '').split(':')
        self.login = webui.get('login', '')
        self.password = webui.get('password', '')
        self.bturl = 'http://{address}:{port}/api?method='.format(address = self.address, port = self.port)
        self.get = self.__request()

    @property
    def connected(self):
        try:
            resp = self.get(self.bturl + 'get_os')
            if isinstance(resp, dict):
                return False
            else:
                return resp.status_code == requests.codes.ok
        except requests.exceptions.ConnectionError as e:
            return False

    def __request(self):
        def inner(url, payload = None):
            if self.login + self.password == '':
                auth = None
            else:
                auth = (self.login, self.password,)
            try:
                return requests.get(url, auth=auth, params=payload).json()
            except requests.exceptions.ConnectionError as e:
                return dict(error = dict(msg = e))
        return inner

    def get_folders(self, secret = None):
        send = {'secret': secret} if secret else None
        return self.get(self.bturl + 'get_folders', send)

    def add_folder(self, directory, secret = None, selective_sync = 0):
        send = {'dir': directory}
        if secret: send['secret'] = secret
        if selective_sync: send['selective_sync'] = selective_sync
        return self.get(self.bturl + 'add_folder', send)

    def remove_folder(self, secret):
        return self.get(self.bturl + 'remove_folder', {'secret': secret})

    def set_file_preferences(self, secret, path, download = True):
        send = {'secret': secret, 'path': path, 'download': 1 if download else 0}
        return self.get(self.bturl + 'set_file_prefs', send)

    def get_files(self, secret, path = None):
        send = {'secret': secret}
        if path: send['path'] = path
        return self.get(self.bturl + 'get_files', send)

    def get_folder_peers(self, secret):
        return self.get(self.bturl + 'get_folder_peers', {'secret': secret})

    def get_secrets(self, secret = None, encryption = False):
        send = {}
        if secret: send['secret'] = secret
        if encryption: send['encryption'] = 'encryption'
        return self.get(self.bturl + 'get_secrets', send)

    def get_folder_preferences(self, secret):
        return self.get(self.bturl + 'get_folder_prefs', {'secret': secret})

    def set_folder_preferences(self, secret, params = immutable_dict):
        return self.get(self.bturl + 'set_folder_prefs', dict({'secret': secret}.items() + params.items()))

    def get_folder_hosts(self, secret):
        return self.get(self.bturl + 'get_folder_hosts', {'secret': secret}) 

    def set_folder_hosts(self, secret, hosts = list()):
        return self.get(self.bturl + 'set_folder_hosts', {'secret': secret, 'hosts': ','.join([a + ':' + b for a, b in hosts])})

    def get_preferences(self):
        return self.get(self.bturl + 'get_prefs')

    def set_preferences(self, preferences = immutable_dict):
        return self.get(self.bturl + 'set_prefs', preferences) 

    def get_os(self):
        return self.get(self.bturl + 'get_os')

    def get_version(self):
        return self.get(self.bturl + 'get_version')

    def get_speed(self):
        return self.get(self.bturl + 'get_speed')

    def shutdown(self):
        msg = self.get(self.bturl + 'shutdown')
        return True if msg['error'] == 0 else msg