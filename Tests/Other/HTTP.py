from bottle import route, run, request

@route('/status/', method='GET')
def platformStatus():

	return 'ONLINE'

@route('/page/', method='GET')
def platformPage():
	
	return 'PAGE'

run(host='192.168.0.11', port=80, debug=True)
