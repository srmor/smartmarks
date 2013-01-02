from smartmarks2 import app
from flask import request
from crossdomain import crossdomain
from smartmarks2.models import Mark, User


@app.route('/api/create', methods=['POST'])
@crossdomain(origin='*')
def api_create():
    title = request.form['title']
    url = request.form['url']
    favicon = request.form['favicon']
    api_key = request.form['api_key']

    cur_user = User.objects.get(api_key=api_key)

    if favicon != ' ':
        new_mark = Mark(
            title=title,
            url=url,
            favicon=favicon,
            type='history',
            user=cur_user.get_id()
        )
    else:
        new_mark = Mark(
            title=title,
            url=url,
            type='history',
            user=cur_user.get_id()
        )

    new_mark.save()

    return new_mark.title
