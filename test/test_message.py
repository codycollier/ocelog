#!/usr/bin/env python

import unittest
import os.path
import sys

test_file_path = os.path.dirname(os.path.abspath(__file__))
ocelog_path = os.path.normpath(os.path.join(test_file_path, "../"))
sys.path.append(ocelog_path)

import ocelog.message
import ocelog_mock


class TestMessage(unittest.TestCase):
    """ Test the ocelog.message module

    """

    #--------------------------------------------------------------------------
    # setup / teardown / utilities
    #--------------------------------------------------------------------------
    def setUp(self):
        """ Perform common setup actions """
        unittest.TestCase.setUp(self)

    def tearDown(self):
        """ Perform common teardown actions """
        unittest.TestCase.tearDown(self)

    #--------------------------------------------------------------------------
    # initialization behavior
    #--------------------------------------------------------------------------
    def test_message_initialization_with_minimal_parameters(self):
        """ Test basic Message object initialization """
        hostname = "myhost"
        appname = "ApplicationManager"
        msg = "service event 17"
        self.omessage = ocelog.message.Message(hostname, appname, msg)
        del self.omessage

    def test_message_can_exist_more_than_once(self):
        """ Test Message object is not singleton """
        hostname = "apphost1"
        appname = "our-app"
        self.omessage = ocelog.message.Message(hostname, appname, msg="some event 1")
        self.omessage2 = ocelog.message.Message(hostname, appname, msg="other event")
        self.assertTrue(self.omessage != self.omessage2)
        del self.omessage
        del self.omessage2

    def test_message_requires_parameters(self):
        """ Test that parameters are required for Message initialization """
        self.assertRaises(TypeError, ocelog.message.Message)

    def test_message_requires_a_hostname_parameter(self):
        """ Test that hostname is required for Message initialization """
        appname = "service1"
        msg = "This is some event here"
        self.assertRaises(TypeError, ocelog.message.Message, appname=appname, msg=msg)

    def test_message_requires_a_appname_parameter(self):
        """ Test that appname string is required for Message initialization """
        hostname = "1.2.3.4"
        msg = "This is some event here"
        self.assertRaises(TypeError, ocelog.message.Message, hostname=hostname, msg=msg)

    def test_message_requires_a_msg_parameter(self):
        """ Test that msg string is required for Message initialization """
        hostname = "192.168.11.11"
        appname = "service1"
        self.assertRaises(TypeError, ocelog.message.Message, hostname=hostname, appname=appname)

    def test_message_initialization_defaults_with_required_parameters(self):
        """ Test default attribute values are correct after minimum initialization """
        # setup with minimum parameters
        hostname = "somehost.example.com"
        appname = "service-app3"
        msg = "the orange juice has reached luke warm temperature"
        self.omessage = ocelog.message.Message(hostname, appname, msg)
        # assert defaults
        self.assertEqual(self.omessage.valid, True)
        self.assertEqual(self.omessage.status, None)
        self.assertEqual(self.omessage.error_msg, None)
        self.assertEqual(self.omessage.hostname, hostname)
        self.assertEqual(self.omessage.appname, appname)
        self.assertEqual(self.omessage.msg, msg)
        self.assertEqual(self.omessage.facility, "user")
        self.assertEqual(self.omessage.priority, "notice")

    def test_message_initialization_with_custom_facility(self):
        """ Test message init will accept custom facility """
        # setup with minimum parameters
        hostname = "somehost.example.com"
        appname = "service-app3"
        msg = "the sky has turned grey"
        self.omessage = ocelog.message.Message(hostname, appname, msg, facility="local3")
        # assert custom attrs
        self.assertEqual(self.omessage.facility, "local3")
        # check the other attrs
        self.assertEqual(self.omessage.valid, True)
        self.assertEqual(self.omessage.status, None)
        self.assertEqual(self.omessage.error_msg, None)
        self.assertEqual(self.omessage.hostname, hostname)
        self.assertEqual(self.omessage.appname, appname)
        self.assertEqual(self.omessage.msg, msg)
        self.assertEqual(self.omessage.priority, "notice")

    def test_message_initialization_with_custom_priority(self):
        """ Test message init will accept custom priority """
        # setup with minimum parameters
        hostname = "ahost.example.com"
        appname = "service53"
        msg = "the sky has turned pink"
        self.omessage = ocelog.message.Message(hostname, appname, msg, priority="err")
        # assert custom attrs
        self.assertEqual(self.omessage.priority, "err")
        # check the other attrs 
        self.assertEqual(self.omessage.valid, True)
        self.assertEqual(self.omessage.status, None)
        self.assertEqual(self.omessage.error_msg, None)
        self.assertEqual(self.omessage.hostname, hostname)
        self.assertEqual(self.omessage.appname, appname)
        self.assertEqual(self.omessage.msg, msg)
        self.assertEqual(self.omessage.facility, "user")

    def test_message_initialization_with_all_custom_parameters(self):
        """ Test message init will accept custom parameters """
        # setup with minimum parameters
        hostname = "1.2.2.3"
        appname = "someapp"
        msg = "the sky has turned blue"
        self.omessage = ocelog.message.Message(hostname, appname, msg, 
                facility="local2", priority="err")
        # assert custom attrs
        self.assertEqual(self.omessage.hostname, hostname)
        self.assertEqual(self.omessage.appname, appname)
        self.assertEqual(self.omessage.msg, msg)
        self.assertEqual(self.omessage.facility, "local2")
        self.assertEqual(self.omessage.priority, "err")
        # check the other attrs
        self.assertEqual(self.omessage.valid, True)
        self.assertEqual(self.omessage.status, None)
        self.assertEqual(self.omessage.error_msg, None)

    #--------------------------------------------------------------------------
    # validation (via initialization)
    #--------------------------------------------------------------------------
    def test_message_validation_will_reject_zero_length_hostname(self):
        """ Test that a bad hostname string will be rejected """
        hostname = ""
        appname = "StrawServer"
        msg = "service alert"
        self.omessage = ocelog.message.Message(hostname, appname, msg)
        self.assertFalse(self.omessage.valid)
        self.assertTrue(len(self.omessage.error_msg) > 1)
        self.assertTrue(self.omessage.error_msg.count("invalid hostname"), 1)
        self.assertEqual(self.omessage.hostname, "invalid")

    def test_message_validation_will_reject_none_hostname(self):
        """ Test that a None hostname will be rejected """
        hostname = None
        appname = "OrangeJ"
        msg = "service alert 45"
        self.omessage = ocelog.message.Message(hostname, appname, msg)
        self.assertFalse(self.omessage.valid)
        self.assertTrue(len(self.omessage.error_msg) > 1)
        self.assertTrue(self.omessage.error_msg.count("invalid hostname"), 1)
        self.assertEqual(self.omessage.hostname, "invalid")

    def test_message_validation_will_reject_zero_length_appname(self):
        """ Test that a bad appname string will be rejected """
        hostname = "10.50.0.1"
        appname = ""
        msg = "graped service has started"
        self.omessage = ocelog.message.Message(hostname, appname, msg)
        self.assertFalse(self.omessage.valid)
        self.assertTrue(len(self.omessage.error_msg) > 1)
        self.assertTrue(self.omessage.error_msg.count("invalid appname"), 1)
        self.assertEqual(self.omessage.appname, "invalid")

    def test_message_validation_will_reject_none_appname(self):
        """ Test that a None appname will be rejected """
        hostname = "servicehost"
        appname = None
        msg = "apple sauce volume is low"
        self.omessage = ocelog.message.Message(hostname, appname, msg)
        self.assertFalse(self.omessage.valid)
        self.assertTrue(len(self.omessage.error_msg) > 1)
        self.assertTrue(self.omessage.error_msg.count("invalid appname"), 1)
        self.assertEqual(self.omessage.appname, "invalid")

    def test_message_validation_will_reject_zero_length_msg(self):
        """ Test that a bad msg string will be rejected """
        hostname = "10.0.0.1"
        appname = "GrapeD"
        msg = ""
        self.omessage = ocelog.message.Message(hostname, appname, msg)
        self.assertFalse(self.omessage.valid)
        self.assertTrue(len(self.omessage.error_msg) > 1)
        self.assertTrue(self.omessage.error_msg.count("invalid msg"), 1)
        self.assertEqual(self.omessage.msg, "invalid")

    def test_message_validation_will_reject_none_msg(self):
        """ Test that a None msg will be rejected """
        hostname = "10.0.0.100"
        appname = "GrapeD"
        msg = None
        self.omessage = ocelog.message.Message(hostname, appname, msg)
        self.assertFalse(self.omessage.valid)
        self.assertTrue(len(self.omessage.error_msg) > 1)
        self.assertTrue(self.omessage.error_msg.count("invalid msg"), 1)
        self.assertEqual(self.omessage.msg, "invalid")

    def test_message_validation_will_reject_invalid_facilities(self):
        """ Test that a invalid facility will be rejected """
        hostname = "10.0.0.100"
        appname = "GrapeApe"
        msg = "client request accepted happily"
        invalid_facilities = (False, "warehouse", 754, "")
        for facility in invalid_facilities:
            self.omessage = ocelog.message.Message(hostname, appname, msg, facility=facility)
            self.assertFalse(self.omessage.valid)
            self.assertTrue(len(self.omessage.error_msg) > 1)
            self.assertTrue(self.omessage.error_msg.count("invalid facility"), 1)
            self.assertEqual(self.omessage.facility, "invalid")

    def test_message_validation_will_reject_invalid_priorities(self):
        """ Test that a invalid priority will be rejected """
        hostname = "koolaid"
        appname = "PitcherDaemon"
        msg = "client request accepted happily"
        invalid_priorities = (True, "superhot", 100, "")
        for priority in invalid_priorities:
            self.omessage = ocelog.message.Message(hostname, appname, msg, priority=priority)
            self.assertFalse(self.omessage.valid)
            self.assertTrue(len(self.omessage.error_msg) > 1)
            self.assertTrue(self.omessage.error_msg.count("invalid priority"), 1)
            self.assertEqual(self.omessage.priority, "invalid")
    
    #--------------------------------------------------------------------------
    # validation 
    #   #ocedebug - should write some direct tests of _validate()
    #--------------------------------------------------------------------------

    #--------------------------------------------------------------------------
    # message writing
    #--------------------------------------------------------------------------
    def test_message_status_when_syslog_write_succeeds(self):
        """ Test message write status when syslog write succeeds """
        writer = ocelog_mock.MockSyslogWriter(write_success=True)
        hostname = "auxhost.example.org"
        appname = "BigService1"
        msg = "the write sky is sunny"
        self.omessage = ocelog.message.Message(hostname, appname, msg)
        self.omessage.write(writer)
        self.assertEqual(self.omessage.status, "success")

    def test_message_status_when_syslog_write_fails(self):
        """ Test message write status when syslog write fails """
        writer = ocelog_mock.MockSyslogWriter(write_success=False)
        hostname = "processing-node-45"
        appname = "someapp"
        msg = "clouds are moving in"
        self.omessage = ocelog.message.Message(hostname, appname, msg)
        self.omessage.write(writer)
        self.assertEqual(self.omessage.status, "write-failure")
        self.assertTrue(len(self.omessage.error_msg) > 1)
        self.assertTrue(self.omessage.error_msg.count("Failure writing message to syslog"), 1)

    #--------------------------------------------------------------------------
    # message printing (for status)
    #--------------------------------------------------------------------------
    def test_message_repr_returns_expected_string_format_for_valid_message(self):
        """ Test repr message will return good string for a valid message"""
        # setup with all custom parameters
        hostname = "10.10.10.1"
        appname = "bigredapp"
        msg = "the sky has turned blue"
        facility = "local3"
        priority = "err"
        self.omessage = ocelog.message.Message(hostname, appname, msg, 
                facility, priority)
        # get repr string and assert
        message_string = repr(self.omessage)
        self.assertEqual(message_string, 
                "[%s] [%s] %s %s: %s" % (facility, priority, hostname, appname, msg))

    def test_message_repr_returns_expected_string_format_for_invalid_message(self):
        """ Test repr message will return good string for an invalid message"""
        # setup with some invalid parameters
        hostname = "10.10.10.1"
        appname = ""                        # invalid
        msg = "the sky has turned blue"
        facility = "['local3']"             # invalid
        priority = "err"
        self.omessage = ocelog.message.Message(hostname, appname, msg, 
                facility, priority)
        # get repr string and assert
        message_string = repr(self.omessage)
        self.assertEqual(message_string, 
                "[%s] [%s] %s %s: %s" % ("invalid", priority, hostname, "invalid", msg))

if __name__=="__main__":

    unittest.main()

