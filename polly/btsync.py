__author__ = 'Blake VandeMerwe'

import os

import requests
import simplejson as json

from collections import namedtuple

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

        if self.login + self.password == '':
            self.pre = self.__without_auth()
        else:
            self.pre = self.__with_auth()


    @property
    def connected(self):
        try:
            return self.pre(self.bturl + 'get_os', dict()).status_code == requests.codes.ok
        except requests.exceptions.ConnectionError as e:
            return False

    def __with_auth(self):
        return lambda url, payload: requests.get(url, auth=(self.login, self.password), params=payload)

    def __without_auth(self):
        return lambda url, payload: requests.get(url, params=payload)

    def get_folders(self, secret = None):
        pass

    def add_folder(self, directory, secret = None, selective_sync = None):
        pass

    def remove_folder(self, secret, path = None):
        pass

    def set_file_preferences(self, secret, path, download):
        pass

    def get_folder_peers(self, secret):
        pass

    def get_secrets(self, secret = None, type = None):
        pass

    def get_folder_preferences(self, secret):
        pass

    def set_folder_preferences(self, secret, params = dict()):
        pass

    def get_folder_hosts(self, secret):
        pass

    def set_folder_hosts(self, secret, hosts = list()):
        pass

    def set_preferences(self, preferences = dict()):
        pass

    def get_os(self):
        pass

    def get_version(self):
        pass

    def get_speed(self):
        pass

    def shutdown(self):
        pass


sync = BtsyncApi(r'../btsync.conf')
print sync.connected