import os
import simplejson as json

def gen_configs(absolute, defined = False):
	if absolute and not defined:
		cwd = os.getcwd()
	elif not absolute and not defined:
		cwd = os.path.curdir
	else:
		cwd = defined

	return {
		'btsync': {
			'path': cwd,
			'type': 'json',
			'config': {
				'storage_path': os.path.join(cwd, 'bin', 'btsync'),
				'use_gui': True,
				'webui': {
					'login': 'api',
					'password': 'secret',
					'listen': '127.0.0.1:8899',
					'api_key': open('BTSYNC_KEY', 'r').read().strip()
				}
			}
		},

		'polly': {
			'path': cwd,
			'type': 'json',
			'config': {
				'default': {
					'autojson': True,
					'debug': True,
					'host': 'localhost',
					'port': 8889,
					'reloader': True,
					'server': 'wsgiref' #gevent
				},
				'sqlite': {
					'db': os.path.join(cwd, 'polly', 'db', 'polly.db'),
					'commit': 'auto'
				},
				'polly': {
					'btsync_path': os.path.join(cwd, 'bin', 'btsync', 'btsync.exe'),
					'btsync_conf_path': os.path.join(cwd, 'btsync.conf'),
					'admin_user': 'default',
					'admin_password': 'default',
					'template_dir': os.path.join(cwd, 'polly', 'templates'),
					'statics_dir': os.path.join(cwd, 'polly', 'static'),
					'allow_symlinks': False
				}
			}
		}
	}

def ini_style(config):
	raise NotImplemented("ini style is not implemented")

def json_style(config):
	with open(config['name'], 'w') as outfile:
		json.dump(config['config'], outfile, encoding = 'ascii', indent = 4)

def generate(only = None, absolute = False):
	config_styles = {
		'ini': ini_style,
		'json': json_style
	}
	configs = gen_configs(absolute)
	for name, config in configs.items():
		if only is not None:
			if name not in only: 
				continue
		config['name'] = '{0}.conf'.format(name)
		config_styles.get(config['type'], None)(config)

if __name__ == '__main__':
	generate(None, True) # generate the configuration files with absolute paths
						 # skip none of them