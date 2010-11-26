""" ocelog.auth - authorization utilitities """

""" 
Copyright 2010 Cody Collier

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import hashlib

import ocelog.config


def generate_mac_token(msg, secret):
    """ Generate a mac token given a msg string and shared secret """
    h = hashlib.md5()
    h.update(msg)
    h.update(secret)
    generated_token = h.hexdigest()
    return generated_token

def authorize_request(request):
    """ Accept a Bottle.request and check the MAC token """
    # short circuit with true if auth is not required
    oconfig = ocelog.config.Config()
    if not oconfig.security.require_token:
        return True
    # compare the mac token given against a generated mac token 
    token = request.environ.get("HTTP_X_TOKEN")
    msg = request.POST.get("msg")
    shared_secret = oconfig.security.shared_secret
    if (token is None) or (msg is None):
        return False
    else:
        expected_token = generate_mac_token(msg, shared_secret)
        return token == expected_token
