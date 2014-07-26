def convert(input, encoding = 'ascii'):
	if isinstance(input, dict):
		return {convert(key): convert(value) for key, value in input.iteritems()}
	elif isinstance(input, list):
		return [convert(e) for e in input]
	elif isinstance(input, unicode):
		return input.encode(encoding)
	else:
		return input