#!/usr/bin/env python

import unittest

import ocelog_functional


class TestRoot(ocelog_functional.OcelogTestCase):
    """ Test the root uri for the ocelog application

    GET @ / -- returns a simple html help document

    """

    def test_get_root(self):
        """ Test GET method on root uri returns simple html help doc """
        response = self.oclient.request("GET", self.root_uri)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.body.startswith("<html>"))
        self.assertEqual(response.body.count("<h2>Ocelog</h2>"), 1)
        self.assertEqual(response.body.count("<h3>The API</h3>"), 1)
        self.assertEqual(response.body.count("</html>"), 1)

    def test_root_invalid_methods(self):
        """ Confirm invalid methods on root uri receive 405 response """
        invalid_methods = ("POST", "PUT", "DELETE")
        for method in invalid_methods:
            response = self.oclient.request(method, self.root_uri)
            self.assertEqual(response.status_code, 405)


if __name__=="__main__":

    unittest.main()
