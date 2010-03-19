import auth
from selector import Selector
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users

def intro_page(environ, start_response): 
    start_response("200 OK", [('Content-type', 'text/html')])
    return ["<a href='" + users.create_logout_url("/") + "'>Logout</a>"]

def main():
    s = Selector([
        ('/', {'GET': intro_page})
        ])

    run_wsgi_app(auth.add_auth(s))

if __name__ == "__main__":
    main()