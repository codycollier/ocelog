#!/usr/bin/env python


import unittest

import ocelog_client


class OcelogTestCase(unittest.TestCase):
    """ A TestCase subclass for use in ocelog functional testing """

    def setUp(self):
        """ Setup the request obj and other common actions """
        # initialize the http request client
        server = "localhost"
        port = 8888
        self.oclient = ocelog_client.OcelogClient(server, port)
        self.oclient.debug = 0
        # set some common vars
        self.root_uri = "/"
        self.log_uri = "/log"

    def tearDown(self):
        """ Tear down the request and other common actions """
        del self.oclient

