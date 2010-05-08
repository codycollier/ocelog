#!/usr/bin/env python
"""exerciser.py - generate requests to exercise the ocelog application

The exerciser will make 10 requests per loop.  If the server requires 
a security token, then enter 1 for token-required.  If it does not, 
then set token-required to 0.  If it doesn't match the server config 
then the assertions will be wrong and the program will exit.

usage:
    ./exerciser.py <host> <port> <loopcount> <token-required>

examples:
    ./exerciser.py localhost 8888 1 0
    ./exerciser.py localhost 8787 10 1

"""

import sys
import random

import ocelog_client

#-----------------------------------------------------------------------------
# test message date for posting to /log
#   (all tokens were generated with shared_secret="beanbags")
#-----------------------------------------------------------------------------
facilities = ("auth", "authpriv", "cron", "daemon", "ftp", "kern", "lpr", 
    "mail", "news", "syslog", "user", "uucp", "local0", "local1",
    "local2", "local3", "local4", "local5", "local6", "local7", "bad-facility")
priorities = ("emerg", "alert", "crit", "err", "warning", 
    "notice", "info", "debug")
hostnames = ("testhost", "webhost1", "10.45.0.2", "192.168.200.34", "mailhost")
appnames = ("app1", "testapp", "somethingD", "my-app", "apiserver", "toaster")
messages = (
    ("this is a service message", "a36e09f84ebe346fc11b7845585e8e7b"),
    ("the coffee pot volume is low", "7d187dda6fcdc56f33832fbbca740808"),
    ("136 requests have been received", "3cc3b99b1a4469d30b9bb1304304861d"),
    ("[database-server-1] error has occured", "a188f0ed4807b6c144c1690d385e784d"),
    ("pid 54, port 7005 has stopped responding", "a27602948bb0cdbe911b4ad0ff592795"),
    ("juice services has started successfully", "db0aca3772d9b3b968481e5c2490a34a"),
    ("the service exited with error code 2", "76d662d029d544bf0e64f10e420cfaca"),
    ("client disconnected", "c100f43c3bfc0563b5e7190e2ab2bd19"),
    ("message received from remote host 23", "b9fc0adc0e1b122572085242f37b9c83"),
    ("234.78 messages per second sent", "65bd276fd9bed67ec5d9332d789dbf37"),
    ("234.78 messages per second sent", "bad-token-bed67ec5d9332d789dbf37"),
    )

def generate_log_request():
    """ Generate a request for post to /log """ 
    facility = random.choice(facilities)
    priority = random.choice(priorities)
    hostname = random.choice(hostnames)
    appname = random.choice(appnames)
    message = random.choice(messages)
    msg = message[0]
    token = message[1]
    params = {'facility':facility, 'priority':priority, 'hostname':hostname, 
        'appname':appname, 'msg':msg}
    return (params, token)


if __name__=="__main__":

    # simple argument handling
    if len(sys.argv) != 5:
        print
        print __doc__
        sys.exit(1)
    else:
        server = sys.argv[1]
        port = sys.argv[2]
        loopcount = int(sys.argv[3])
        token_required = int(sys.argv[4])

    # header
    print
    print "preparing to exercise app"
    print "server: http://%s:%s" % (server, port)
    print "loops: %s (10 requests per loop)" % (loopcount)
    print

    # setup the client
    oclient = ocelog_client.OcelogClient(server, port)
    oclient.debug = 0

    # run the test requests
    for i in range(1,loopcount+1):
        response = oclient.request("GET", "/")
        assert(response.status_code == 200)
        response = oclient.request("GET", "/")
        assert(response.status_code == 200)
        for r in range(8):
            (params, token) = generate_log_request()
            headers = {}
            headers['x-token'] = token
            response = oclient.request("POST", "/log", params, headers)
            if params['facility'] == "bad-facility":
                assert(response.status_code == 400)
            elif token_required and token.startswith("bad-token"):
                assert(response.status_code == 400)
            else:
                assert(response.status_code == 201)
        print "completed loop: %s" % i

    # footer
    print 
    print "sent %s requests" % (loopcount * 10)
    print "done exercising"
    print


