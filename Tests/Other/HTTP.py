from bottle import route, run, request

@route('/status/', method='GET')
def platformStatus():

	return '\nONLINE\n'

@route('/page/', method='GET')
def platformPage():
	
	return '\nPAGE\n'

@route('/porn/', method='GET')
def platformPorn():

	return '\nVIDEO\n'

run(host='192.168.0.11', port=80, debug=True)
