from song import Songs
from util import add_auth, tpl_file
from selector import Selector
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

def intro_page(environ, start_response): 
    start_response("200 OK", [('Content-type', 'text/html')])

    v = {
        'logout_url': users.create_logout_url("/")
    }
    return [template.render(tpl_file('index.html'), v)]

def songs_list(environ, start_response): 
    songdao = []
    for song in Songs().getall():
        songdao.append({'id': song.meta.get('id'), 'title': song.meta.get('title')})
    
    songdao.sort(lambda x,y: cmp(x['title'].lower(), y['title'].lower()))

    v = {
        'songs': songdao
    }

    start_response("200 OK", [('Content-type', 'text/html')])
    return template.render(tpl_file('list.html'), v)

def main():
    s = Selector([
        ('/songs', {'GET': songs_list}),
        ('/', {'GET': intro_page})
        ])

    run_wsgi_app(s)

if __name__ == "__main__":
    main()