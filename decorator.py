from functools import wraps
from flask import request, Response

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'amazon' and password == 'candidate'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    "<!DOCTYPE HTML PUBLIC '-//IETF//DTD HTML 2.0//EN'>"
    "<html><head>"
    "<title>401 Authorization Required</title>"
    "</head><body>"
    "<h1>Authorization Required</h1>"
    "<p>This server could not verify that you"
    "are authorized to access the document"
    "requested.  Either you supplied the wrong"
    "credentials (e.g., bad password), or your"
    "browser doesn't understand how to supply"
    "the credentials required.</p>"
    "<hr>"
    "<address>Apache/2.2.29 (Amazon) Server at 54.199.147.29 Port 80</address>"
    "</body></html>",401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
