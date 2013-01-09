from smartmarks import app
import unittest
from smartmarks.models import Invite


class SmartMarksTest(unittest.TestCase):

    def setUp(self):
        app.config['MONGODB_DB'] = 'test'
        app.config['TEST'] = True
        self.app = app.test_client()

        self.Invite = Invite

    def tearDown(self):
        for invite in self.Invite.objects:
            invite.delete()

    def test_signed_out_home(self):
        request = self.app.get('/')
        assert 'Bookmarks that save themselves' in request.data

    def test_not_invited(self):
        request = self.app.get('/sign-up')
        assert 'need to have a valid invite code.' in request.data

    def test_invited(self):
        invite = self.Invite(code="testing")
        invite.save()

        request = self.app.get('/sign-up?invite=testing')
        assert '<input type="password" name="confirm-password" placeholder="confirm password">' in request.data

    def test_sign_in_out(self):
        request = self.app.post('/sign-in', data=dict(
            email="tests@smartmarks.co",
            password="wetestcode"
        ), follow_redirects=True)

        assert 'Sign Out' in request.data

        request = self.app.get('/sign-out', follow_redirects=True)

        assert 'Sign In' in request.data


if __name__ == '__main__':
    unittest.main()
