from bottle import route, run, request

@route('/status/', method='GET')
def platformStatus():

	return 'ONLINE'

run(host='192.168.0.10', port=80, debug=True)
