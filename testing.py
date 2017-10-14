from unittest import TestCase
from model import connect_to_db, db
from server import app
from flask import session

class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):

        result = self.client.get('/')
        self.assertIn('<h1>Welcome!</h1>', result.data)

    def test_login(self):

        result = self.client.get('/login')
        self.assertIn('<h1>LogIn</h1>', result.data)

    def test_register(self):

        result = self.client.get('/register')
        self.assertIn('<h1>Register</h1>', result.data)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to the database
        connect_to_db(app, "postgresql:///testtext")

        # Create tables and add sample data
        db.create_all()
        testtext()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"username": shakira, "password": "123go"},
                                  follow_redirects=True)
        self.assertIn("You are a valued user", result.data)        


if __name__ == '__main__':

	import unittest

	unittest.main()
    