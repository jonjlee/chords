import logging
import webob
from song import Song
from util import read_request_body, add_auth, accept_types
from selector import Selector
from google.appengine.ext.webapp.util import run_wsgi_app

def get_song(environ, start_response):
    id = environ['selector.vars']['id']
    text, content_type = Songs.read(id, environ['CONTENT_TYPE'])
    if text:
        start_response("200 OK", [('Content-type', content_type)])
        return [text]

    start_response("404 Not Found", [('Content-type', 'text-plain')])
    return []

def put_song(environ, start_response):
    id = environ['selector.vars']['id']
    lines = read_request_body(environ)
    start_response("204 No Content", [])
    return []

def preview_text(environ, start_response):
    lines = read_request_body(environ)
    song = Song(lines)
    start_response("200 OK", [('Content-type', 'text/html')])
    return [song.get_html()]

def preview_form(environ, start_response):
    req = webob.Request(environ)  
    meta = {
        'title': req.POST['title'],
        'subtitle': req.POST['subtitle'],
        'byline': req.POST['byline']}
    lines = [''] + req.POST['text'].split('\r\n')
    song = Song(lines, meta)
    start_response("200 OK", [('Content-type', 'text/html')])
    return [song.get_html()]

def delete_song(environ, start_response):
    start_response("204 No Content", [])
    return []

def list_songs(environ, start_response):
    start_response("200 OK", [('Content-type', 'text/plain')])
    return ["hello"]


def main():
    mappings = [
        ('/preview',    {'POST': accept_types([
                                 ("text/plain", preview_text),
                                 ("application/x-www-form-urlencoded", preview_form)])}),
        ('/songs/{id}', {'GET': get_song, 
                         'PUT': put_song,
                         'DELETE': delete_song}),
        ('/songs[/]',   {'GET': list_songs})]

    s = Selector(mappings, prefix='/d')

    # run_wsgi_app(auth.add_auth(s))
    run_wsgi_app(s)

if __name__ == "__main__":
    main()