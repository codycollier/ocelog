""" ocelog.auth - authorization utilitities

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
