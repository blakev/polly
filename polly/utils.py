__author__ = 'Blake'

import os
import subprocess

def batch_restart(conf):
    ins = '''
taskkill /im btsync.exe /f
{btsync_path} /config {btsync_conf_path}'''.format(
        btsync_path = os.path.join(os.getcwd(), conf('polly.btsync_path', '')),
        btsync_conf_path = os.path.join(os.getcwd(), conf('polly.btsync_conf_path', '')))

    batch_file = os.path.join(os.getcwd(), 'scripts', 'btsync.bat')
    with open(batch_file, 'w') as f:
        f.write(ins)

    outs = subprocess.call([batch_file], shell=False)
    print outs, batch_file

    return True if outs == 0 else batch_file

def shell_restart(conf):
    raise NotImplementedError('needs linux implementation in polly/utils.py')

def force_btsync_restart(conf):
    if 'nt' in os.name:
        fn = batch_restart
    else:
        fn = shell_restart

    ret = fn(conf)

    if ret is True:
        return True
    else:
        raise SystemError('Could not launch btsync on your system, check: {0}'.format(ret))