from selector import EnvironDispatcher
from google.appengine.api import users

def login(environ, start_response):
    start_response("302 Found", [('Location', users.create_login_url(environ.get('PATH_INFO','')))])

def not_authenticated(environ):
    return users.get_current_user() == None
def default_rule(environ): 
    return True
    
def add_auth(app):
    rules = [(not_authenticated, login), (default_rule, app)]
    return EnvironDispatcher(rules)
