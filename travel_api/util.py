import re


def get_token(auth_string):
    token_object = re.match("^Bearer\s+(.*)", auth_string)
    if token_object:
        return token_object.group(1)
    return None
