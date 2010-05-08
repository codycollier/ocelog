""" ocelog_client -- a simple httplib wrapper for ocelog functional testing

"""

import httplib
import urllib


class OcelogResponse(object):
    """ A simple wrapper around httplib.HTTPResponse"""

    def __init__(self, http_response):
        """ Accept and parse an httplib.HTTPResponse object """
        self.status_code = http_response.status
        self.status_msg = http_response.reason
        self.POST = {}
        for key,value in http_response.getheaders():
            self.POST[key] = value
        self.body = http_response.read()


class OcelogClient(object):
    """ A simple wrapper around httplib.HTTPConnetion """

    def __init__(self, server, port):
        """ Initialize the request object with common configs """
        self.server = server
        self.port = port
        self.debug = 0

    def request(self, method, path, parameters=None, headers={}):
        """ Perform a request and return an OcelogResponse object """
        # setup the http connection
        conn = httplib.HTTPConnection(self.server, self.port)
        conn.set_debuglevel(self.debug)
        headers = headers
        body = None
        # If parameters were provided, form-urlencode them and set headers accordingly
        if parameters is not None:
            headers['Content-Type'] = "application/x-www-form-urlencoded"
            body = urllib.urlencode(parameters)
        # make the request and return a response
        conn.request(method, path, body, headers)
        response = OcelogResponse(conn.getresponse())
        conn.close()
        return response



