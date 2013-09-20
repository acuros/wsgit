
def application1(environ, start_response):
    import json
    start_response('200 OK', [('Content-Type', 'application/json')])
    yield '{}'
