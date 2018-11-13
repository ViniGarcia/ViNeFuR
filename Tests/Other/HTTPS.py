from bottle import route, run, request

@route('/status/', method='GET')
def platformStatus():

	return 'ONLINE'

run(host='localhost', port=443, debug=True)
