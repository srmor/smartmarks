from flask import abort, session, render_template
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
            if fn.__name__ == 'index':
                return render_template('loggedout/index.html', auth=False, page="Home")
            else:
                abort(401)
    return decorator


def getCss(file):
    return '/static/css/' + file


def getJs(file):
    return '/static/js/' + file


def getImg(file):
    return '/static/img/' + file

def get_result_num_by_page(request):
    if request.args.get('pg'):
        page = int(request.args.get('pg'))
    else:
        page = 1

    start_result = 20 * (page - 1)
    end_result = 20 * page

    return page, start_result, end_result
