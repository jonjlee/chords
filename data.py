import auth
from selector import Selector
from google.appengine.ext.webapp.util import run_wsgi_app

def get_song(environ, start_response):
    id = environ['selector.vars']['id']
    start_response("200 OK", [('Content-type', 'text/plain;annotated=true')])
    return ["song " + id]
def put_song(environ, start_response):
    start_response("200 OK", [('Content-type', 'text/plain')])
    return ["hello"]
def delete_song(environ, start_response):
    start_response("200 OK", [('Content-type', 'text/plain')])
    return ["hello"]
def list_songs(environ, start_response):
    start_response("200 OK", [('Content-type', 'text/plain')])
    return ["hello"]


def main():
    mappings = [
        ('/songs/{id}', {'GET': get_song, 'PUT': put_song, 'DELETE': delete_song}),
        ('/songs[/]', {'GET': list_songs})
        ]
    s = Selector(mappings, prefix='/d')

    run_wsgi_app(auth.add_auth(s))

if __name__ == "__main__":
    main()