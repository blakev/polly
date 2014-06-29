__author__ = 'Blake'

import os
import subprocess




def conf(app):
    def inner(x, y = ''):
        return app.config.get(x, y)
    return inner

def batch_restart(conf, cwd = os.getcwd()):
    ins = '''
tasklist /fi "imagename eq btsync.exe" | find ":" > nul
if errorlevel 1 taskkill /f /im "btsync.exe"
{btsync_path} /config {btsync_conf_path}'''.strip().format(
        btsync_path = conf('polly.btsync_path', ''),
        btsync_conf_path = conf('polly.btsync_conf_path', ''))

    batch_file = os.path.join(os.getcwd(), 'scripts', 'btsync.bat')
    with open(batch_file, 'w') as f:
        f.write(ins)

    proc = subprocess.Popen(batch_file, cwd=cwd, shell=False)
    out, err = proc.communicate()
    return True if not err else batch_file

def shell_restart(conf):
    raise NotImplementedError('needs linux implementation in polly/utils.py')

def force_btsync_restart(conf, cwd):
    if 'nt' in os.name:
        fn = batch_restart
    else:
        fn = shell_restart

    ret = fn(conf, cwd)

    if ret is True:
        return True
    else:
        raise SystemError('Could not launch btsync on your system, check: {0}'.format(ret))