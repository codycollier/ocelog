#!/usr/bin/env python

import unittest

import ocelog_functional


class TestLog(ocelog_functional.OcelogTestCase):
    """ Test the log uri of the ocelog app """

    def test_get_log(self):
        """ Test that GET on log uri returns simple html help doc """
        pass
        response = self.oclient.request("GET", self.log_uri)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.body.startswith("<html>"))
        self.assertEqual(response.body.count("<h2>Ocelog</h2>"), 1)
        self.assertEqual(response.body.count("<h3>The API</h3>"), 1)
        self.assertEqual(response.body.count("</html>"), 1)
   
    def test_log_invalid_methods(self):
        """ Confirm invalid methods on root uri receive 405 response """
        invalid_methods = ("PUT", "DELETE")
        for method in invalid_methods:
            response = self.oclient.request(method, self.log_uri)
            self.assertEqual(response.status_code, 405)

    def test_log_post_with_valid_message(self):
        """ Test a POST of a valid message to the log uri results in a 201 """
        params = {}
        params['appname'] =  "test-app-a"
        params['hostname'] = "testhost-a"
        params['msg'] = "the service was restarted"
        response = self.oclient.request("POST", self.log_uri, params)
        self.assertEqual(response.status_code, 201)



if __name__=="__main__":

    unittest.main()


