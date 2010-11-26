""" ocelog.message - The message data structure and parsing utilities """

""" 
Copyright 2010 Cody Collier

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import ocelog.config


def parse_request(request):
    """ Accept a bottle.request object and return a Message object

    This function is responsible for taking an incoming HTTP request, 
    extracting the request components, and returning a Message object.

    Currently, the parser expects application/x-www-form-urlencoded data in 
    an HTTP POST.  The data is automatically extracted by bottle and placed
    in bottle.request.POST.  In the future, the parser may allow for xml or 
    other data formats in the body.

    The parser performs no validation.
    """
    hostname = request.POST.get("hostname")
    if hostname is None:
        hostname = request.environ['REMOTE_ADDR']
    appname = request.POST.get("appname")
    msg = request.POST.get("msg", None)
    facility = request.POST.get("facility")
    priority = request.POST.get("priority")
    return Message(hostname, appname, msg, facility, priority)


class MessageException(Exception):
    """ A generic Message exception class """

class Message(object):
    """ Parse, validate, and write an incoming log message

    This class is the data structure for the incoming log message.  Instead of 
    being called directly, the object is usually created and returned by a 
    parse_*_request function.  This decouples the web server request object from
    the Message class and could allow for future integrate with other web 
    servers.

    At initialization time, the incoming message is validated.  The boolean 
    flag Message.valid is set accordingly.  The Message.status is populated if 
    there is a "validation-failure".

    After init and confirmation of a valid message, the write() method should
    be called.  If the write succeeds, then Message.status will be set to 
    "success".  If it fails, then Message.status will be set to "write-failure".

    For any of the error states of _Message, a human friendly error message will
    be written to _Message.error_msg.  This can be used in a response header 
    such as x-ocelog-error.
    
    required message data:
      hostname - The fqdn, hostname, or ip of the source host
      appname - The application name or identifier to be logged
      msg - The message to be logged
    optional message data:
      facility - an overriding syslog facility
      priority - an overriding syslog priority
    """

    valid_facilities = ("auth", "authpriv", "cron", "daemon", "ftp", "kern",
        "lpr", "mail", "news", "syslog", "user", "uucp", "local0", "local1",
        "local2", "local3", "local4", "local5", "local6", "local7")

    valid_priorities = ("emerg", "alert", "crit", "err", "warning", "notice",
        "info", "debug")

    def __init__(self, hostname, appname, msg, facility=None, priority=None):
        """ Validate and Authenticate the message """
        # get externals
        self.config = ocelog.config.Config()
        # set defaults
        self.valid = False
        self.status = None
        self.error_msg = None
        if facility is None:
            facility = self.config.message.default_facility
        if priority is None:
            priority = self.config.message.default_priority
        # validate
        self._validate(hostname, appname, msg, facility, priority)
        if not self.valid:
            self.status = "validation-failure"

    def _validate(self, hostname, appname, msg, facility, priority):
        """ Validate the message data and set flags accordingly """
        # hostname validation
        if (hostname is None) or (not len(hostname) > 0):
            self.error_msg = "Message included invalid hostname string"
            self.hostname = "invalid"
        else:
            self.hostname = hostname
        # appname validation
        if (appname is None) or (not len(appname) > 0):
            self.error_msg = "Message included invalid appname string"
            self.appname = "invalid"
        else:
            self.appname = appname
        # msg validation
        if (msg is None) or (not len(msg) > 0):
            self.error_msg = "Message included invalid msg string"
            self.msg = "invalid"
        else:
            self.msg = msg
        # facility validation
        if facility not in self.valid_facilities:
            self.error_msg = "Message included invalid facility"
            self.facility = "invalid"
        else:
            self.facility = facility
        # priority validation
        if priority not in self.valid_priorities:
            self.error_msg = "Message included invalid priority"
            self.priority = "invalid"
        else:
            self.priority = priority
        # if everything passed, mark as valid
        if "invalid" not in (self.hostname, self.appname, self.msg, 
                self.facility, self.priority):
            self.valid = True
        return

    def write(self, writer):
        """ Write the message to all enabled writers """
        retval = writer.write(self)
        if retval == True:
            self.status = "success"
        else:
            self.status = "write-failure"
            self.error_msg = "Failure writing message to syslog"
        return

    def __repr__(self):
        """ Return a well formed string version of the message """
        parts = []
        parts.append("[%s]" % (self.facility))
        parts.append("[%s]" % (self.priority))
        parts.append("%s %s:" % (self.hostname, self.appname))
        parts.append("%s" % (self.msg))
        line = " ".join(parts)
        return line




