import datetime
from flask import url_for
from smartmarks import db


class MarkVisit(db.EmbeddedDocument):
    ''' One user visit to a Mark '''
    date = db.DateTimeField(default=datetime.datetime.now, required=True)


class Mark(db.Document):
    ''' A history or bookmark item created by the user '''
    visited_at = db.ListField(db.EmbeddedDocumentField('MarkVisit'))
    title = db.StringField(max_length=255, required=True)
    url = db.StringField(max_length=2000, required=True)
    favicon = db.StringField(max_length=400, required=False)
    type = db.StringField(max_length=8, required=True)
    user_id = db.StringField(max_length=500, required=True)

    def __unicode__(self):
        return self.title

    def get_url(self):
        return url_for('mark', kwargs={"url": self.url})

    def get_icon(self):
        return url_for('mark_icon', kwargs={"favicon": self.favicon})


class User(db.Document):
    ''' An SmartMarks user '''
    sign_up_date = db.DateTimeField(default=datetime.datetime.now, required=True)
    email = db.StringField(max_length=100, required=True)
    password = db.StringField(max_length=60, required=True)
    api_key = db.StringField(max_length=32, required=True)

    def get_id(self):
        return unicode(self.id)


class Invite(db.Document):
    ''' A unique invite code during invite-only beta '''
    date = db.DateTimeField(default=datetime.datetime.now, required=True)
    code = db.StringField(max_length=10, required=True)
    claimed = db.BooleanField(default=False)

    def get_id(self):
        return unicode(self.id)
