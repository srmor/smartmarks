from flask import session


def check_auth():
    if 'email' in session:
        return True
    else:
        return False
