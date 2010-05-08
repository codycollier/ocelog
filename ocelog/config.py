""" ocelog.config - the configuration management module


"""


import ConfigParser
import os.path
import socket


class ConfigException(Exception):
    """ A simple configuration exception class """


class _ServerConfig(object):
    """ Data structure for the server related configurations """

    def __init__(self):
        """ Initialize the object with the default configurations """
        self._port = 8888
        self._host = "localhost"

    @property
    def port(self):
        """ Return the port number """
        return self._port

    @port.setter
    def port(self, port):
        """ Validate and override the port attribute """
        port = int(port)
        if port > 0 and port < 65556:
            self._port = port
        else:
            raise ConfigException, "port must be between 0 and 65536"

    @property
    def host(self):
        """ Return the host where the server should listen """
        return self._host

    @host.setter
    def host(self, host):
        """ Validate and override the host attribute """
        # ocedebug - this only says it resolves, not that its local
        try:
            socket.gethostbyname(host)
            self._host = host
        except:
            raise ConfigException, "host must be a valid and resolvable hostname"


class _MessageConfig(object):
    """ Data structure for the Message configurations """

    valid_facilities = ("auth", "authpriv", "cron", "daemon", "ftp", "kern", 
            "lpr", "mail", "news", "syslog", "user", "uucp", "local0", "local1",
            "local2", "local3", "local4", "local5", "local6", "local7")

    valid_priorities = ("emerg", "alert", "crit", "err", "warning", "notice", 
            "info", "debug")

    def __init__(self):
        """ Initialize the object with the default configurations """
        self._default_facility = "user"
        self._default_priority = "notice"

    @property
    def default_facility(self):
        """ Return the attr default_facility """
        return self._default_facility

    @default_facility.setter
    def default_facility(self, new_facility):
        """ Validate and set an overriding default_facility """
        if new_facility in self.valid_facilities:
            self._default_facility = new_facility
        else:
            raise ConfigException, "default_facility must be a valid syslog facility"

    @property
    def default_priority(self):
        """ Return the default_priority attr """
        return self._default_priority

    @default_priority.setter
    def default_priority(self, new_priority):
        """ Validate and set an overriding default_priority """
        if new_priority in self.valid_priorities:
            self._default_priority = new_priority
        else:
            raise ConfigException, "default_priority must be a valid syslog priority"


class _SyslogConfig(object):
    """ Data structure for the SyslogWriter configurations """

    def __init__(self):
        """ Initialize the object with the default configurations """
        self._enabled = False

    @property
    def enabled(self):
        """ Return the enabled attr """
        return self._enabled

    @enabled.setter
    def enabled(self, new_value):
        """ Validate and set an overriding enabled """
        if new_value in ("True", "False"):
            self._enabled = eval(new_value)
        elif new_value in (True, False):
            self._enabled = new_value
        else:
            raise ConfigException, "syslog.enabled must be set to true or false"


class _SecurityConfig(object):
    """ Data structure for the security and authorization configs """

    def __init__(self):
        """ Initialize the object with the default configurations """
        self._require_token = False
        self._shared_secret = None

    @property
    def require_token(self):
        """ Return the require_token attr """
        return self._require_token

    @require_token.setter
    def require_token(self, new_value):
        """ Validate and set an overriding require_token """
        if new_value in ("True", "False"):
            self._require_token = eval(new_value)
        elif new_value in (True, False):
            self._require_token = new_value
        if self._require_token == True and self._shared_secret == None:
            raise ConfigException, "A shared secret must be set if require_token is true"

    @property
    def shared_secret(self):
        """ Return the shared_secret attr """
        return self._shared_secret

    @shared_secret.setter
    def shared_secret(self, new_value):
        """ Validate and set an overriding shared_secret """
        if len(new_value) >= 8:
            self._shared_secret = new_value
        else:
            raise ConfigException, "shared_secret must be at least 8 characters in length"


class Config(object):
    """ A data structure and manager for application configurations

    The Config() class consolidates several specialized configuration objects 
    and the management of overriding config defaults with a config file.  Upon 
    initialization, if there is no config file passed in, then the objects are 
    initialized and the defaults are used.  If a config file is passed in, then 
    it is read and any overriding user settings are applied.
    """

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwds):
        """ Enforce a singleton patter """
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, config_file=None):
        """ Initialized each config and apply overrides as needed """

        if self._initialized is False:
            # setup configs and defaults
            self.server = _ServerConfig()
            self.message = _MessageConfig()
            self.syslog = _SyslogConfig()
            self.security = _SecurityConfig()
            # if a config file is provided, validate and apply overriding configs
            if config_file is not None:
                self._apply_config_file(config_file)
            # we don't want to overwrite configs so set a flag
            self._initialized = True

    def _apply_config_file(self, config_file):
        """ Retrieve and set any overriding configurations from config file
       
        Validation of any given option/attribute is handled by a setter method 
        in its configuration class.
        """
        # Open the config file
        if not os.path.exists(config_file):
            raise ConfigException, "configuration file does not exist"
        config = ConfigParser.ConfigParser()
        try:
            config.readfp(open(config_file))
        except:
            raise ConfigException, "unable to read configuration file"

        # configuration sections and options
        sections = {}
        sections["server"] = ("port", "host")
        sections["message"] = ("default_facility", "default_priority")
        sections["syslog"] = ("enabled",)
        sections["security"] = ("shared_secret", "require_token")

        # iterate through each section and each option, and if that option 
        #  is available in the config file, get it and override the attribute
        for section,options in sections.items():
            for option in options:
                if config.has_option(section, option):
                    new_value = config.get(section, option)
                    section_config = self.__dict__[section]
                    setattr(section_config, option, new_value)


