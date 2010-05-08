#!/usr/bin/env python

import unittest
import os.path
import sys

test_file_path = os.path.dirname(os.path.abspath(__file__))
ocelog_path = os.path.normpath(os.path.join(test_file_path, "../"))
sys.path.append(ocelog_path)

import ocelog_mock
import ocelog.writer


class TestWriter(unittest.TestCase):
    """ Test the Writer module for ocelog 
    
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
    def test_syslog_writer_is_singleton(self):
        """ Confirm singleton behavior is enforced for SyslogWriter """
        self.owriter = ocelog.writer.SyslogWriter()
        self.owriter2 = ocelog.writer.SyslogWriter()
        self.assertEqual(self.owriter, self.owriter2)

    def test_syslog_writer_is_initialized_with_correct_defaults(self):
        """ Test init of SyslogWriter results in correct defaults """
        self.owriter = ocelog.writer.SyslogWriter()
        self.assertEqual(self.owriter.config.syslog.enabled, False)

    #--------------------------------------------------------------------------
    # write
    #--------------------------------------------------------------------------
    def test_syslog_writer_will_return_success_when_disabled(self):
        """ Test that disabled=True results in success for all writes """
        self.owriter = ocelog.writer.SyslogWriter()
        self.owriter.config.syslog.enabled = False
        message = ocelog_mock.MockMessage(msg="the client has disconnected")
        success = self.owriter.write(message)
        self.assertTrue(success)

    # ocedebug
    # the syslog methods all return None.  
    # Should it be mocked and that part better tested?



if __name__=="__main__":

    # run all tests in random order
    #import random
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestMessage)
    #random.shuffle(suite._tests)
    #unittest.TextTestRunner(verbosity=2).run(suite)

    unittest.main()


