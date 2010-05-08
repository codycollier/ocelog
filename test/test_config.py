#!/usr/bin/env python

import unittest
import os.path
import sys

test_file_path = os.path.dirname(os.path.abspath(__file__))
ocelog_path = os.path.normpath(os.path.join(test_file_path, "../"))
sys.path.append(ocelog_path)
import ocelog.config


class TestConfig(unittest.TestCase):
    """ Test the ocelog.config module

    Test config files can be found in the ./testdata/ directory and 
    are used to test variations in the Config class behavior.
    """

    #--------------------------------------------------------------------------
    # setup / teardown / utilities
    #--------------------------------------------------------------------------
    def setUp(self):
        """ Perform common setup actions """
        unittest.TestCase.setUp(self)
        self.test_data_path = os.path.join(test_file_path, "./testdata/")
        # This is a hack to 'delete' the singleton and allow it to be 
        # reinitialized if it was initialized by a test in one of the other 
        # suites.  This is required when this test module is run as a part of 
        # the complete suites in ./run_all_tests.py.
        oc = ocelog.config.Config()
        oc._initialized = False
        del oc

    def tearDown(self):
        """ Perform common teardown actions """
        unittest.TestCase.tearDown(self)
        # This is a hack to 'delete' the singleton after the test is done and 
        # allow the next test in line to reinitialized the config object.
        oc = ocelog.config.Config()
        oc._initialized = False
        del oc

    #--------------------------------------------------------------------------
    # invalid config file variations
    #--------------------------------------------------------------------------
    def test_nonexistent_config_file_will_raise_exception(self):
        """ Passing Config a non-existent file should result in exception """
        config_file = "no-such-file"
        oconfig = ocelog.config
        self.assertRaises(oconfig.ConfigException, oconfig.Config, config_file)

    # ocedebug -- this test works locally, but that file can't be commited to svn
    def skip_test_unreadable_config_file_will_raise_exception(self):
        """ Passing Config an unreadable file should result in exception """
        config_file = "%s/config_unreadable.conf" % self.test_data_path
        oconfig = ocelog.config
        self.assertRaises(oconfig.ConfigException, oconfig.Config, config_file)

    #--------------------------------------------------------------------------
    # overriding default configuration options with sample config files
    #--------------------------------------------------------------------------
    def test_override_for_all_the_server_options(self):
        """ Test an override of all of the server option defaults """
        config_file = "%s/config_server_overrides_all.conf" % self.test_data_path
        oconfig = ocelog.config.Config(config_file)
        self.assertEqual(oconfig.server.port, 7777)          # override of "8888"
        self.assertEqual(oconfig.server.host, "127.0.0.1")   # override of "localhost"

    def test_override_of_subset_of_server_options(self):
        """ Test an override of a subset of the server option defaults """
        config_file = "%s/config_server_overrides_partial.conf" % self.test_data_path
        oconfig = ocelog.config.Config(config_file)
        self.assertEqual(oconfig.server.port, 5555)          # override of "8888"     
        self.assertEqual(oconfig.server.host, "localhost")   # default

    def test_override_of_all_the_message_options(self):
        """ Test an override of all of the message option defaults """
        config_file = "%s/config_message_overrides_all.conf" % self.test_data_path
        oconfig = ocelog.config.Config(config_file)
        self.assertEqual(oconfig.message.default_facility, "local1")     # override of "user"
        self.assertEqual(oconfig.message.default_priority, "warning")    # override of "notice"

    def test_override_of_subset_of_message_options(self):
        """ Test an override of a subset of the message option defaults """
        config_file = "%s/config_message_overrides_partial.conf" % self.test_data_path
        oconfig = ocelog.config.Config(config_file)
        self.assertEqual(oconfig.message.default_facility, "local5")     # override of "user"
        self.assertEqual(oconfig.message.default_priority, "notice")     # default

    def test_override_of_all_the_syslog_options(self):
        """ Test an override of all of the syslog option defaults """
        config_file = "%s/config_syslog_overrides_all.conf" % self.test_data_path
        oconfig = ocelog.config.Config(config_file)
        self.assertEqual(oconfig.syslog.enabled, True) # override of "False" 

    def test_override_of_subset_of_syslog_options(self):
        """ Test an override of a subset of the syslog option defaults """
        config_file = "%s/config_syslog_overrides_partial.conf" % self.test_data_path
        oconfig = ocelog.config.Config(config_file)
        self.assertEqual(oconfig.syslog.enabled, True)    # override of "False" 

    def test_override_of_all_the_security_options(self):
        """ Test an override of all of the security option defaults """
        config_file = "%s/config_security_overrides_all.conf" % self.test_data_path
        oconfig = ocelog.config.Config(config_file)
        self.assertEqual(oconfig.security.require_token, True)          # override of False
        self.assertEqual(oconfig.security.shared_secret, "grapejuice")  # override of None

    def test_override_of_subset_of_security_options_is_not_allowed(self):
        """ Test that shared_secret must be set if require_token is overriden to true """
        config_file = "%s/config_security_overrides_partial.conf" % self.test_data_path
        self.assertRaises(ocelog.config.ConfigException, ocelog.config.Config, config_file)

    def test_manual_override_of_boolean_options(self):
        """ Test the boolean validators accept true booleans and not just strings """
        config_file = "%s/config_defaults.conf" % self.test_data_path
        oconfig = ocelog.config.Config(config_file)
        self.assertEqual(oconfig.syslog.enabled, False)                  # default
        self.assertEqual(oconfig.security.require_token, False)          # default
        # now manually override
        oconfig.syslog.enabled = True
        oconfig.security.shared_secret = "grapefruitjuice"              # required to enable require_token
        oconfig.security.require_token = True
        self.assertEqual(oconfig.syslog.enabled, True)                  # override of False
        self.assertEqual(oconfig.security.require_token, True)          # override of False

    def test_override_of_mixed_set_of_options(self):
        """ Test an override of a mix of options across sections """
        config_file = "%s/config_mixed_overrides_1.conf" % self.test_data_path
        oconfig = ocelog.config.Config(config_file)
        self.assertEqual(oconfig.server.port, 7777)                      # override "8888"     
        self.assertEqual(oconfig.server.host, "localhost")               # default
        self.assertEqual(oconfig.message.default_facility, "local3")     # override of "user"
        self.assertEqual(oconfig.message.default_priority, "err")        # override of "notice"
        self.assertEqual(oconfig.syslog.enabled, False)                  # default
        self.assertEqual(oconfig.security.require_token, False)          # default
        self.assertEqual(oconfig.security.shared_secret, "fruitpunch")   # override of None

    #--------------------------------------------------------------------------
    # overriding configuration options with invalid values
    #--------------------------------------------------------------------------

    #ocedebug - need to test the raising of ConfigExceptions

    #--------------------------------------------------------------------------
    # initialization and instance behavior
    #--------------------------------------------------------------------------
    def test_config_defaults_are_set_when_no_config_file_is_provided(self):
        """ Test that defaults are set properly when no config file exists """
        # create an instance of the Config class with no config file
        oconfig = ocelog.config.Config()
        # assert that the Server defaults are correct
        self.assertEqual(oconfig.server.port, 8888)
        self.assertEqual(oconfig.server.host, "localhost")
        # assert that the Message defaults are correct
        self.assertEqual(oconfig.message.default_facility, "user")
        self.assertEqual(oconfig.message.default_priority, "notice")
        # assert that the SyslogWriter defaults are correct
        self.assertEqual(oconfig.syslog.enabled, False)
        # assert that the security defaults are correct
        self.assertEqual(oconfig.security.require_token, False)
        self.assertEqual(oconfig.security.shared_secret, None)

    def test_config_class_is_singleton(self):
        """ Test that the singleton trait is enforced with the Config class """
        oconfig = ocelog.config.Config()
        oconfig2 = ocelog.config.Config()
        self.assertEqual(oconfig, oconfig2)

    def test_config_object_cannot_be_reinitialized_with_new_config(self):
        """ Test that the configs are not reinitialized with every call """
        config_file_1 = "%s/config_defaults.conf" % self.test_data_path
        oconfig = ocelog.config.Config(config_file_1)
        config_file_2 = "%s/config_defaults_all_overriden.conf" % self.test_data_path
        oconfig2 = ocelog.config.Config(config_file_2)
        self.assertEqual(oconfig, oconfig2)
        # assert the the non-default values in the second call were skipped
        self.assertEqual(oconfig2.server.port, 8888)
        self.assertEqual(oconfig2.server.host, "localhost")
        # assert that the Message defaults are correct
        self.assertEqual(oconfig2.message.default_facility, "user")
        self.assertEqual(oconfig2.message.default_priority, "notice")
        # assert that the SyslogWriter defaults are correct
        self.assertEqual(oconfig2.syslog.enabled, False)
        # assert that the security defaults are correct
        self.assertEqual(oconfig.security.require_token, False)
        self.assertEqual(oconfig.security.shared_secret, None)


if __name__=="__main__":

    # run all tests in random order
    #import random
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestConfig)
    #random.shuffle(suite._tests)
    #unittest.TextTestRunner(verbosity=2).run(suite)

    unittest.main()

