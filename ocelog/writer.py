""" ocelog.writer - The message writer(s)

"""


import syslog

import ocelog.config


class WriterException(Exception):
    """ A generic exception class for the Writer """


class SyslogWriter(object):
    """ Accept Message() objects and pass them to syslog

    """

    _instance = None

    def __new__(cls, *args, **kwds):
        """ Enforce singleton behavior """
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        """ Initialize the SyslogWriter and prepare for writing """
        self.config = ocelog.config.Config()

    def write(self, message):
        """ Accept ocelog.message.Message and write to syslog """
        if not self.config.syslog.enabled:
            return True
        else:
            try:
                log_facility = eval("syslog.LOG_%s" % message.facility.upper())
                log_priority = eval("syslog.LOG_%s" % message.priority.upper())
                ident = "%s %s" % (message.hostname, message.appname)
                syslog.openlog(ident)
                syslog.syslog(log_facility | log_priority, message.msg)
                syslog.closelog()
                return True
            except:
                return False





