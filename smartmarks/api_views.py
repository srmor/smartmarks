from smartmarks import app
from flask import request, Response
from crossdomain import crossdomain
from smartmarks.models import MarkVisit, Mark, User
from flask.ext.bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/api/create', methods=['POST'])
@crossdomain(origin='*')
def api_create():
    title = request.form['title']
    url = request.form['url']
    favicon = request.form['favicon']
    type = request.form['type']
    api_key = request.form['api_key']

    cur_user = User.objects.get(api_key=api_key)

    # If the url has been visited before just add a new MarkVisit
    try:
        mark = Mark.objects.filter(url=url)[0]

        mark_visit = MarkVisit()
        mark.visited_at.append(mark_visit)

        if mark.type != type and mark.type == 'history':
            mark.type = type

        if mark.title != title and type == 'bookmark':
            mark.title = title

        mark.save()

        return mark.title

    # If url hasn't been visited before then create a new mark
    except:

        if favicon != ' ':
            new_mark = Mark(
                title=title,
                url=url,
                favicon=favicon,
                type=type,
                user_id=cur_user.get_id()
            )
        else:
            new_mark = Mark(
                title=title,
                url=url,
                type=type,
                user_id=cur_user.get_id()
            )

        mark_visit = MarkVisit()
        new_mark.visited_at.append(mark_visit)

        new_mark.save()

        return new_mark.title


@app.route('/api/sign-in', methods=['POST'])
@crossdomain(origin='*')
def api_sign_in():
    email = request.form['email']
    password = request.form['password']

    try:
        cur_user = User.objects.get(email=email)
        if bcrypt.check_password_hash(cur_user.password, password):
            return cur_user.api_key
        else:
            return Response('Try Again', status=401, mimetype='application/json')
    except:
        return Response('Try Again', status=401, mimetype='application/json')
