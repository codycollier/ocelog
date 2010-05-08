#!/usr/bin/env python
""" ocelog.wsgi - the wsgi application built upon the bottle micro-framework

The application is available as: ocelog.wsgi.application
"""

import sys
import os.path

from ocelog.bottle import route
from ocelog.bottle import response
from ocelog.bottle import request
from ocelog.bottle import abort
from ocelog.bottle import send_file
from ocelog.bottle import default_app
import ocelog.message
import ocelog.auth
import ocelog.writer



#-----------------------------------------------------------------------------
# bottle.default_app() / ocelog.wsgi.application / routers and handlers 
#-----------------------------------------------------------------------------
file_path = os.path.dirname(os.path.abspath(__file__))
doc_path = os.path.normpath(os.path.join(file_path, "../doc/"))

@route('/', method='GET')
@route('/log', method='GET')
def show_help_doc():
    """ Return a help page to the user """
    #return static_file("help.htm", root=doc_path)
    return send_file("help.htm", root=doc_path)

@route('/log', method='POST')
def log():
    """ Accept a message and send it to syslog

    1> filter the request by headers
    2> authorize the request if required (sec token)
    3> validate the incoming message
    4> write the message

    """
    # Confirm support for incoming content-type
    content_type = request.environ['CONTENT_TYPE']
    if content_type != "application/x-www-form-urlencoded":
        response.header["x-ocelog-error"] = "Data must be x-www-form-urlencoded"
        response.status = 415
        return
    # Authorize the request
    authorized = ocelog.auth.authorize_request(request)
    if not authorized:
        response.header['x-ocelog-error'] = "Request failed authorization"
        response.status = 400
        return
    # Extract and validate the message
    message = ocelog.message.parse_request(request)
    if not message.valid:
        response.header["x-ocelog-error"] = message.error_msg
        response.status = 400
        return
    # If valid, attempt the write
    owriter = ocelog.writer.SyslogWriter()
    message.write(owriter)
    if message.status == "success":
        response.status = 201
    else:
        response.header["x-ocelog-error"] = message.error_msg
        response.status = 400
        return

@route('/', method='POST')
@route('/', method='PUT')
@route('/', method='DELETE')
@route('/log', method='PUT')
@route('/log', method='DELETE')
def invalid_method():
    """ Return a 405 for invalid methods on valid uris """
    response.status = 405
    return


# make the wsgi application available for servers to access
application = default_app()




