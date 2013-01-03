from smartmarks2 import app
from flask import request, redirect, render_template, url_for, session, abort
from smartmarks2.models import Mark, User, Invite
from flask.ext.bcrypt import Bcrypt
import hashlib
import datetime
from random import randint
from functools import wraps
import re

bcrypt = Bcrypt(app)


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


@app.route('/')
@logged_in
def index(user_id):
    marks = Mark.objects.filter(user=user_id).order_by('-visited_at')

    return render_template('index.html', auth=True, page="index", marks=marks)


@app.errorhandler(401)
def no_auth(e):
    return render_template('not-allowed.html')


@app.route('/history')
@logged_in
def history(user_id):
    marks = Mark.objects.filter(type='history', user=user_id).order_by('-visited_at')

    return render_template('index.html', auth=True, page="history", marks=marks)


@app.route('/bookmarks')
@logged_in
def bookmarks(user_id):
    marks = Mark.objects.filter(type='bookmark', user=user_id).order_by('-visited_at')

    return render_template('index.html', auth=True, page="bookmarks", marks=marks)


@app.route('/search')
@logged_in
def search(user_id):
    if request.args.get('search'):
        search = request.args.get('search').lower().strip()
        marks = Mark.objects.filter(title=re.compile(re.escape(search), re.IGNORECASE), user=user_id).order_by('-visited_at')

        return render_template('index.html', auth=True, page="search", search=search, marks=marks)
    else:
        return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
@logged_in
def create(user_id):
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']

        new_mark = Mark(
            title=title,
            url=url,
            type='bookmark',
            user=user_id
        )

        new_mark.save()

        return redirect(url_for('index'))
    else:
        return render_template('create.html', auth=True, page="create")


@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if 'email' in session:
        return render_template('signed_in.html', auth=True, page="sign in")
    else:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            try:
                cur_user = User.objects.get(email=email)
                if bcrypt.check_password_hash(cur_user.password, password):
                    session['email'] = email

                    return redirect((url_for('index')))
                else:
                    return render_template('sign_in.html', auth=False, page="sign in", error=True)

            except:
                return render_template('sign_in.html', auth=False, page="sign in", error=True)

        return render_template('sign_in.html', auth=False, page="sign in")


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if 'email' in session:
        return render_template('signed_in.html', auth=True, page="sign up")
    else:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            password_confirm = request.form['confirm-password']
            invite = request.form['invite']

            if password != password_confirm:
                return render_template('sign_up.html', auth=False, page="sign up", error="Your passwords do not match. Try again.")

            try:
                User.objects.get(email=email)
                return render_template('sign_up.html', auth=False, page="sign up", error='An account with that email already exists.')
            except:

                try:
                    # Check if invite code is valid and if valid set it as claimed
                    code = Invite.objects.get(code=invite)
                    code.update(set__claimed=True)

                    # Create the new user
                    cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    rand_int = str(randint(0, 200))
                    api_key = hashlib.md5()
                    api_key.update(cur_time + email + rand_int)

                    new_user = User(
                        email=email,
                        password=bcrypt.generate_password_hash(password),
                        api_key=api_key.hexdigest()
                    )
                    new_user.save()

                    session['email'] = email

                    return redirect(url_for('index'))
                except:
                    return render_template('sign_up.html', auth=False, page="sign up", error='Your invite is invalid.')

        elif request.args.get('invite'):
            code = request.args.get('invite')

            try:
                invite = Invite.objects.get(code=code, claimed=False)
                return render_template('sign_up.html', auth=False, page="sign up", invite=code)
            except:
                return render_template('not-allowed.html', auth=False, page="sign up")

        else:
            return render_template('not-allowed.html', auth=False, page="sign up")

        return render_template('sign_up.html', auth=False, page="sign up")


@app.route('/sign-out')
@logged_in
def sign_out(user_id):
    session.pop('email')
    return redirect(url_for('index'))
