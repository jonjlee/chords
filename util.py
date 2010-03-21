import os
import re
from selector import EnvironDispatcher
from google.appengine.api import users

tpl_path = os.path.dirname(__file__) + "/templates"
title_to_id_pattern = re.compile('[^A-Za-z0-9-]')

def title_to_id(title):
    return title_to_id_pattern.sub('-', title)

def login(environ, start_response):
    start_response("302 Found", [('Location', users.create_login_url(environ.get('PATH_INFO','')))])

def not_acceptable(environ, start_response):
    start_response("406 Not Acceptable", [])

def unsupported_media_type(environ, start_response):
    start_response("415 Unsupported Media Type", [])

def not_authenticated(environ):
    return users.get_current_user() == None

def default_rule(environ): 
    return True
    
def add_auth(app):
    rules = [(not_authenticated, login), (default_rule, app)]
    return EnvironDispatcher(rules)

def check_for_content_type(content_type):
    return lambda environ: (environ['CONTENT_TYPE'] == None and v == None) or (environ['CONTENT_TYPE'] != None and environ['CONTENT_TYPE'].lower() == content_type.lower())

# content_types is a list of tuples (content-type, app), e.g. [('text/plain', handle_text), ('application/json', handle_json)]
def accept_types(content_types):
    rules = [(default_rule, unsupported_media_type)]
    for (content_type,app) in content_types:
        rules.insert(0, (check_for_content_type(content_type), app))
    return EnvironDispatcher(rules)

# content_types is a list of tuples (content-type, app), e.g. [('text/plain', handle_text), ('application/json', handle_json)]
def produce_types(content_types):
    rules = [(default_rule, not_acceptable)]
    for (content_type,app) in content_types:
        rules.insert(0, (check_for_content_type(content_type), app))
    return EnvironDispatcher(rules)

def read_request_body(environ):
    lines = []
    for line in environ['wsgi.input']:
        lines.append(line)
    return lines
    
def tpl_file(tpl):
    return os.path.join(tpl_path, tpl)
