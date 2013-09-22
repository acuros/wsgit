from djangoproject.djangoproject.wsgi import application as django_application

def various_status_application(environ, start_response):
    import json
    status = environ.get('QUERY_STRING') or '200 OK'
    start_response(status, [('Content-Type', 'application/json')])
    
    yield '{}'
