#!/usr/bin/env python

import unittest

import ocelog_functional


class TestLogToken(ocelog_functional.OcelogTestCase):
    """ Test the log uri of the ocelog app with require_token enabled 
    
    Alert!: The server must have the following config for this test module 
    to work correctly:
        [security]
        require_token: True
        shared_secret: beanbag

    The tests will succeed and silently ignore the x-token header if 
    require_token is disabled.
    """

    triples = (
        ("this is a service message", "beanbags", "a36e09f84ebe346fc11b7845585e8e7b"),
        ("the coffee pot volume is low", "beanbags", "7d187dda6fcdc56f33832fbbca740808"),
        ("136 requests have been received", "beanbags", "3cc3b99b1a4469d30b9bb1304304861d"),
        ("[database-server-1] error has occured", "beanbags", "a188f0ed4807b6c144c1690d385e784d"),
        ("pid 54, port 7005 has stopped responding", "beanbags", "a27602948bb0cdbe911b4ad0ff592795"),
        ("juice services has started successfully", "beanbags", "db0aca3772d9b3b968481e5c2490a34a"),
        )

    def test_log_post_with_valid_message_and_token(self):
        """ Test a POST of a valid message with a valid token results in a 201 """
        for msg,secret,token in self.triples:
            params = {}
            params['appname'] =  "web_service"
            params['msg'] = msg
            headers = {'X-Token':token,}
            response = self.oclient.request("POST", self.log_uri, params, headers)
            self.assertEqual(response.status_code, 201)


if __name__=="__main__":

    unittest.main()


