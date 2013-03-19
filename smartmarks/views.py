from smartmarks import app
from flask import request, redirect, render_template, url_for, session
from smartmarks.models import Mark, User, Invite, SignUp
from flask.ext.bcrypt import Bcrypt
import hashlib
import datetime
from random import randint
from fxns import logged_in, get_result_num_by_page
import re
import math

bcrypt = Bcrypt(app)


# Error handlers
@app.errorhandler(401)
def no_auth(e):
    return render_template('not-allowed.html')


# Pages to view Marks
@app.route('/', methods=['GET', 'POST'])
def index():
    # TODO: make this login check more elegant
    if 'email' in session:
        # If user is signed in get the user's id
        email = session['email']
        cur_user = User.objects.get(email=email)

        result_nums = get_result_num_by_page(request)
        page = result_nums[0]
        start_result = result_nums[1]
        end_result = result_nums[2]

        marks = Mark.objects.filter(user_id=cur_user.get_id()).order_by('-visited_at')[start_result:end_result]
        mark_num = Mark.objects.filter(user_id=cur_user.get_id()).order_by('-visited_at').count()
        total_pages = int(math.ceil(mark_num / 20)) + 1

        return render_template('index.html', auth=True, page="Home", marks=marks, cur_page=page, last_page=total_pages)
    else:
        # if user is signing up to be notified when smarmarks launches
        if request.method == 'POST':
            email = request.form['email']

            try:
                sign_up = SignUp.objects.get(email=email)
            except:
                sign_up = SignUp(
                    email=email
                )

                sign_up.save()

            return render_template('loggedout/index.html', auth=False, page="Home", signed_up=True)

        else:
            return render_template('loggedout/index.html', auth=False, page="Home")


@app.route('/history')
@logged_in
def history(user_id):
    result_nums = get_result_num_by_page(request)
    page = result_nums[0]
    start_result = result_nums[1]
    end_result = result_nums[2]

    marks = Mark.objects.filter(type='history', user_id=user_id).order_by('-visited_at')[start_result:end_result]
    mark_num = Mark.objects.filter(type='history', user_id=user_id).order_by('-visited_at').count()
    total_pages = int(math.ceil(mark_num / 20)) + 1

    return render_template('index.html', auth=True, page="History", marks=marks, cur_page=page, last_page=total_pages)


@app.route('/bookmarks')
@logged_in
def bookmarks(user_id):
    result_nums = get_result_num_by_page(request)
    page = result_nums[0]
    start_result = result_nums[1]
    end_result = result_nums[2]

    marks = Mark.objects.filter(type='bookmarks', user_id=user_id).order_by('-visited_at')[start_result:end_result]
    mark_num = Mark.objects.filter(type='bookmarks', user_id=user_id).order_by('-visited_at').count()
    total_pages = int(math.ceil(mark_num / 20)) + 1

    marks = Mark.objects.filter(type='bookmark', user_id=user_id).order_by('-visited_at')

    return render_template('index.html', auth=True, page="Bookmarks", marks=marks, cur_page=page, last_page=total_pages)


@app.route('/search')
@logged_in
def search(user_id):
    if request.args.get('search'):
        result_nums = get_result_num_by_page(request)
        page = result_nums[0]
        start_result = result_nums[1]
        end_result = result_nums[2]

        search = request.args.get('search').lower().strip()

        marks = Mark.objects.filter(title=re.compile(re.escape(search), re.IGNORECASE), user_id=user_id).order_by('-visited_at')[start_result:end_result]
        mark_num = Mark.objects.filter(title=re.compile(re.escape(search), re.IGNORECASE), user_id=user_id).order_by('-visited_at').count()
        total_pages = int(math.ceil(mark_num / 20)) + 1

        return render_template('index.html', auth=True, page="Search", search=search, marks=marks, cur_page=page, last_page=total_pages)
    else:
        return redirect(url_for('index'))


# Pages to handle auth
@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if 'email' in session:
        return render_template('signed_in.html', auth=True, page="Sign In")
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
                    return render_template('sign_in.html', auth=False, page="Sign In", error=True)

            except:
                return render_template('sign_in.html', auth=False, page="Sign In", error=True)

        return render_template('sign_in.html', auth=False, page="Sign In")


# TODO: abstract more of the sign up view code
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # if a user is signed in
    if 'email' in session:
        return render_template('signed_in.html', auth=True, page="Sign Up")
    else:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            password_confirm = request.form['confirm-password']
            invite = request.form['invite']

            if password != password_confirm:
                return render_template('sign_up.html', auth=False, page="Sign Up", invite=invite, error="Your passwords do not match. Please enter it again.")
            elif len(password) < 8:
                return render_template('sign_up.html', auth=False, page="Sign Up", invite=invite, error="Your password needs to be at least 8 characters long.")

            try:
                User.objects.get(email=email)
                return render_template('sign_up.html', auth=False, page="Sign Up", error='An account with that email already exists.')
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
                    return render_template('not-invited.html', auth=False, page="Sign Up")

        elif request.args.get('invite'):
            code = request.args.get('invite')

            # check if invite code is valid and render the sign up form if it is
            try:
                invite = Invite.objects.get(code=code, claimed=False)
                return render_template('sign_up.html', auth=False, page="Sign Up", invite=code)
            # otherwise show the not invited error page
            except:
                return render_template('not-invited.html', auth=False, page="Sign Up")

        # if the user visits the page without an invite at all show them the not invited error page
        else:
            return render_template('not-invited.html', auth=False, page="Sign Up")

        return render_template('sign_up.html', auth=False, page="sign up")


@app.route('/sign-out')
@logged_in
def sign_out(user_id):
    session.pop('email')
    return redirect(url_for('index'))
