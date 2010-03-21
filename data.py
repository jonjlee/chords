import webob
import songformat
from song import Songs, Song
from util import read_request_body, add_auth, accept_types, title_to_id
from selector import Selector
from google.appengine.ext.webapp.util import run_wsgi_app

def get_song(environ, start_response):
    id = environ['selector.vars']['id']
    text, content_type = Songs().read(id, environ.get('HTTP_ACCEPT'))
    if text:
        start_response("200 OK", [('Content-type', content_type)])
        return [text]

    start_response("404 Not Found", [])
    return ["Song not found."]

def put_song(environ, start_response):
    id = environ['selector.vars']['id']
    song = Song(read_request_body(environ))
    Songs().write(id, song)
    start_response("204 No Content", [])
    return []

def preview_text(environ, start_response):
    song = Song(read_request_body(environ))
    start_response("200 OK", [('Content-type', 'text/html')])
    return [song.get_html()]

def preview_form(environ, start_response):
    req = webob.Request(environ)  
    meta = {
        'title': req.POST['title'].replace(':', '.'),
        'subtitle': req.POST['subtitle'].replace(':', '.'),
        'byline': req.POST['byline'].replace(':', '.')}
    lines = [''] + req.POST['text'].split('\r\n')
    song = Song(lines, meta)

    if req.POST.get('action') == 'Save':
        id = title_to_id(req.POST['title'])
        Songs().write(id, song)
        start_response("302 Found", [('Location', '/d/songs/' + id)])
        return []
    else:
        start_response("200 OK", [('Content-type', 'text/html')])
        return [song.get_html()]

def delete_song(environ, start_response):
    id = environ['selector.vars']['id']
    Songs().delete(id)
    start_response("204 No Content", [])
    return []

def list_songs(environ, start_response):
    start_response("200 OK", [('Content-type', 'text/plain')])
    ids = map(lambda x: x+'\n', Songs().getids())
    return ids


def main():
    mappings = [
        ('/preview',    {'POST': accept_types([
                                 ("text/plain", preview_text),
                                 ("application/x-www-form-urlencoded", preview_form)])}),
        ('/songs/{id}', {'GET': get_song, 
                         'PUT': accept_types([
                                  ("text/plain", put_song)]),
                         'DELETE': delete_song}),
        ('/songs[/]',   {'GET': list_songs})]

    s = Selector(mappings, prefix='/d')

    run_wsgi_app(s)

if __name__ == "__main__":
    main()