""" ocelog_mock - Mock objects used by the module unit tests for ocelog

"""


class MockMessage(object):
    """ A simple mock of ocelog.message.Message """

    def __init__(self, hostname="1.2.3.4", appname="mockapp", 
            msg="big event 43", status="success", facility="user", 
            priority="notice"):
        
        """ Set some mock data """
        self.status = status
        self.hostname = hostname
        self.appname = appname
        self.msg = msg
        self.facility = facility
        self.priority = priority

    def __repr__(self):
        """ Return the message as a string """
        line = ', '.join([self.status, self.facility, self.priority, 
                self.hostname, self.appname, self.msg])
        return line

class MockBottleRequest(object):
    """ A simple mock of bottle.request """

    def __init__(self, hostname=None, appname=None, msg=None, facility=None, 
            priority=None, token=None):
        """ Return a populated request object """
        self.POST = {}
        self.POST['hostname'] = hostname
        self.POST['appname'] = appname
        self.POST['msg'] = msg
        self.POST['facility'] = facility
        self.POST['priority'] = priority
        self.environ = {}
        if token is not None:
            self.environ['HTTP_X_TOKEN'] = token

class MockSyslogWriter(object):
    """ A simple mock of ocelog.writer.SyslogWriter """

    _instance = None

    def __new__(cls, *args, **kwds):
        """ Enforce singleton behavior """
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, write_success=True):
        """ Init and determine write() behavior """
        self.write_success = write_success

    def write(self, message):
        """ A mock syslog write """
        return self.write_success



