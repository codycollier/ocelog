#!/usr/bin/env python

import unittest
import os.path
import sys

test_file_path = os.path.dirname(os.path.abspath(__file__))
ocelog_path = os.path.normpath(os.path.join(test_file_path, "../"))
sys.path.append(ocelog_path)

import ocelog.auth
import ocelog_mock


class TestAuth(unittest.TestCase):
    """ Test the ocelog.auth module

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
    # generate_mac_token
    #--------------------------------------------------------------------------
    def test_token_generator_requires_msg_and_secret_string(self):
        """ Test the token generator requires a msg string and a secret string """
        self.assertRaises(TypeError, ocelog.auth.generate_mac_token)
        self.assertRaises(TypeError, ocelog.auth.generate_mac_token, msg="a message")
        self.assertRaises(TypeError, ocelog.auth.generate_mac_token, secret="a secret")

    def test_token_generator_returns_expected_tokens(self):
        """ Test the token generator returns expected tokens """
        # (message, secret, token)
        triples = []
        triples.append(("this is a service message", "blanket", "bfc6745732b6d0c640510fcdd75698b7"))
        triples.append(("the coffee pot volume is low", "porchlite", "d1ed63df8f2ce2da3463004cddd761a6"))
        triples.append(("136 requests have been received", "this is a shared secret", "9fa7f76f8b90b46ff53a983b2e89acc3"))
        triples.append(("[database-server-1] error has occured", "color328wheels", "c0256202937fbfb419d2e96e6793832b"))
        triples.append(("pid 54, port 7005 has stopped responding", "guitarstring4", "df7707e8c88db8b54372a4d5e1b84d0e"))
        triples.append(("juice services has started successfully", "123456789",  "63eb56135de40df0f62608bdde1b19bd"))
        for msg,secret,expected_token in triples:
            generated_token = ocelog.auth.generate_mac_token(msg, secret)
            self.assertEqual(expected_token, generated_token)

    #--------------------------------------------------------------------------
    # authorize_request
    #--------------------------------------------------------------------------
    def test_authorize_request_is_true_if_require_token_is_disabled(self):
        """ Test authorization succeeds if require_token is disabled """
        request = ocelog_mock.MockBottleRequest()
        authorized = ocelog.auth.authorize_request(request)
        self.assertTrue(authorized)

    def test_authorize_request_is_false_if_token_is_not_set(self):
        """ Test authorization will fail if token is not present """
        # override config manually
        oconfig = ocelog.config.Config()
        oconfig.security.shared_secret = "porchlite"
        oconfig.security.require_token = True
        # setup
        msg = "this is a service message"
        token = None
        request = ocelog_mock.MockBottleRequest(msg=msg, token=token)
        # attempt auth
        authorized = ocelog.auth.authorize_request(request)
        self.assertFalse(authorized)

    def test_authorize_request_fails_with_bad_token_and_msg(self):
        """ Test request authorization fails with known bad data """
        # override config manually
        oconfig = ocelog.config.Config()
        oconfig.security.shared_secret = "porchlite"
        oconfig.security.require_token = True
        # setup
        msg = "the coffee pot volume is low."   # just added a period
        token = "d1ed63df8f2ce2da3463004cddd761a6"
        request = ocelog_mock.MockBottleRequest(msg=msg, token=token)
        # attempt authorization
        authorized = ocelog.auth.authorize_request(request)
        self.assertFalse(authorized)

    def test_authorize_request_succeeds_with_good_token_and_msg(self):
        """ Test request authorization succeeds with known good data """
        # override config manually
        oconfig = ocelog.config.Config()
        oconfig.security.shared_secret = "porchlite"
        oconfig.security.require_token = True
        # setup
        msg = "the coffee pot volume is low"
        token = "d1ed63df8f2ce2da3463004cddd761a6"
        request = ocelog_mock.MockBottleRequest(msg=msg, token=token)
        # attempt authorization
        authorized = ocelog.auth.authorize_request(request)
        self.assertTrue(authorized)







if __name__=="__main__":

    unittest.main()

