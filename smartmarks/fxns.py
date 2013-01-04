from flask import abort, session
from functools import wraps
from smartmarks.models import User


def logged_in(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        if 'email' in session:
            # If user is signed in get the user's id
            email = session['email']
            cur_user = User.objects.get(email=email)

            return fn(cur_user.get_id())
        else:
            abort(401)
    return decorator
