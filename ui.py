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

def main():
    s = Selector([
        ('/', {'GET': intro_page})
        ])

    run_wsgi_app(s)

if __name__ == "__main__":
    main()