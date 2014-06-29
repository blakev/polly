__author__ = 'Blake'

import time
import gevent
import requests

from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

class StatusNamespace(BaseNamespace, BroadcastMixin):
    def recv_connect(self):
        def get_stats():
            while True:
                btsync_stats = requests.get('http://localhost:8085/api/btsync_stats').text
                self.emit('message', {
                    'status': 'ok!',
                    'time': time.time(),
                    'sync_stats': btsync_stats})

                gevent.sleep(5.0)

        self.spawn(get_stats)

    def recv_disconnect(self):
        pass