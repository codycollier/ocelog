#!/usr/bin/env python
""" Ocelog - An http interface to syslog


"""

import sys
import os.path

import ocelog.wsgi


if __name__=="__main__":

    # simple arg handling
    valid_servers = ("dev", "eventlet", "cherrypy")
    server_type = "dev"
    if len(sys.argv) == 2:
        if sys.argv[1] in valid_servers:
            server_type = sys.argv[1]

    # Initialize the configuration
    import ocelog.config
    oconfig = ocelog.config.Config(config_file="doc/config_defaults.conf")
    #oconfig = ocelog.config.Config()


    if server_type == "eventlet":
        import eventlet
        from eventlet import wsgi
        ocelog_app = ocelog.wsgi.application
        wsgi.server(eventlet.listen(
            (oconfig.server.host, oconfig.server.port)), 
            ocelog_app)

    elif server_type == "cherrypy":
        from ocelog import bottle
        ocelog_app = ocelog.wsgi.application
        bottle.run(reloader=False, server=bottle.CherryPyServer,
                host=oconfig.server.host, port=oconfig.server.port,
                app=ocelog_app)

    elif server_type == "gevent":
        import gevent.wsgi
        ocelog_app = ocelog.wsgi.application
        gapp = gevent.wsgi.WSGIServer((oconfig.server.host, 
            oconfig.server.port), ocelog.wsgi.application)
        gapp.serve_forever()

    elif server_type == "dev":
        #-------------------------------------------------------------------------
        # simple server good for development and running the functional tests
        #-------------------------------------------------------------------------
        # enable this to return tracebacks to the client
        # bottle.debug(True)
        # enable this to start real syslog writing
        # oconfig.syslog.enabled = True
        # enable these items to run test/functional/test_log_token.py
        # oconfig.security.shared_secret = "beanbags"
        # oconfig.security.require_token = True

        from ocelog import bottle
        ocelog_app = ocelog.wsgi.application
        bottle.run(reloader=False, 
                host=oconfig.server.host, port=oconfig.server.port,
                app=ocelog.wsgi.application)

