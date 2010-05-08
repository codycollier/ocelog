#!/usr/bin/env python

import unittest
import os.path
import sys

test_file_path = os.path.dirname(os.path.abspath(__file__))
ocelog_path = os.path.normpath(os.path.join(test_file_path, "../"))
sys.path.append(ocelog_path)

import ocelog.message
import ocelog_mock


class TestRequestParsers(unittest.TestCase):
    """ Test the request parsers in the ocelog.message module

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
    # parse_request
    #--------------------------------------------------------------------------
    def test_parser_correctly_passes_valid_required_parameters(self):
        """ Test request parser correctly passes basic msg to Message """
        hostname = "front-server-a"
        appname = "app-manager"
        msg = "event 458 just occured"
        request = ocelog_mock.MockBottleRequest(hostname, appname, msg)
        self.omessage = ocelog.message.parse_request(request)
        # assert required attrs
        self.assertEqual(self.omessage.hostname, hostname)
        self.assertEqual(self.omessage.appname, appname)
        self.assertEqual(self.omessage.msg, msg)
        # check the other attrs too
        self.assertEqual(self.omessage.valid, True)
        self.assertEqual(self.omessage.status, None)
        self.assertEqual(self.omessage.error_msg, None)
        self.assertEqual(self.omessage.facility, "user")
        self.assertEqual(self.omessage.priority, "notice")

    def test_parser_correctly_passes_valid_custom_facility(self):
        """ Test request parser correctly passes custom facility to Message """
        hostname = "webhost2"
        appname = "otherapp"
        msg = "action 234 has completed"
        request = ocelog_mock.MockBottleRequest(hostname, appname, msg, facility="local0")
        self.omessage = ocelog.message.parse_request(request)
        # assert custom attr
        self.assertEqual(self.omessage.facility, "local0")
        # check the other attrs too
        self.assertEqual(self.omessage.valid, True)
        self.assertEqual(self.omessage.status, None)
        self.assertEqual(self.omessage.error_msg, None)
        self.assertEqual(self.omessage.hostname, hostname)
        self.assertEqual(self.omessage.appname, appname)
        self.assertEqual(self.omessage.msg, msg)
        self.assertEqual(self.omessage.priority, "notice")

    def test_parser_correctly_passes_valid_custom_priority(self):
        """ Test request parser correctly passes custom priority to Message """
        hostname = "webhost1"
        appname = "someapp"
        msg = "action 123 has completed"
        request = ocelog_mock.MockBottleRequest(hostname, appname, msg, priority="debug")
        self.omessage = ocelog.message.parse_request(request)
        # assert custom attr
        self.assertEqual(self.omessage.priority, "debug")
        # check the other attrs too
        self.assertEqual(self.omessage.valid, True)
        self.assertEqual(self.omessage.status, None)
        self.assertEqual(self.omessage.error_msg, None)
        self.assertEqual(self.omessage.hostname, hostname)
        self.assertEqual(self.omessage.appname, appname)
        self.assertEqual(self.omessage.msg, msg)





if __name__=="__main__":

    unittest.main()

