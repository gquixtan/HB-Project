from unittest import TestCase
from model import connect_to_db, db, test_texts
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
        connect_to_db(app, "postgresql:///testtexts")

        # Create tables and add sample data
        db.create_all()
        test_texts()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_login(self):
        """Test login page."""

        with self.client as c:
            result = self.client.post("/login",
                                      data={"username": "shakira", "password": "123go"},
                                      follow_redirects=True)

            self.assertEqual(session["username"], "shakira")
            self.assertIn("Hi Shakira, Welcome!", result.data)

    def test_login_with_none(self):
        """Test in case user typed the wrong password or username."""

        with self.client as c:
            result = self.client.post("/login",
                                      data={"username": "fergalicious", "password": "123"},
                                      follow_redirects=True)

            self.assertIn("Oops, did you type the right username or password?", result.data)


    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"]=1

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn('user_id', session)
            self.assertIn('You were successfully logged out', result.data)


    def test_register(self):
        """Test register route."""

        with self.client as c:

            result = self.client.post("/register",
                                      data={"firstname": "Me","lasttname": "Myself", "username": "I", "password": "123go"},
                                      follow_redirects=True)

            self.assertEqual(session["username"], "I")
            self.assertIn("Texts", result.data)
            self.assertIn("Log out", result.data)
            self.assertIn("Hi Me, Welcome! ", result.data)
            self.assertIn("SUBMIT YOUR TEXT USING A KEYWORD", result.data)
    
    def test_register_with_exisiting_user(self):
        """Test register with user that already existes in db."""

        with self.client as c:
            with c.session_transaction() as sess: 
                sess["user_id"]=2

            result = self.client.post("/register",
                                    data={"firstname": "Fergie","lasttname": "Licious", "username": "fergalicious", "password": "123go"},
                                    follow_redirects=True)   


    def test_keyword(self):
        """Test getkeyword route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess["fname"]="Fergie"
                sess["user_id"]=2
                sess["username"]="fergalicious"

            result = self.client.get("/getkeyword", 
                                    query_string={"keyword":"this", "phone":"1231236669", "date":"2017,3,23"},
                                    follow_redirects=True)

            self.assertEqual(session["fname"], "Fergie")
            self.assertEqual(session['user_id'], 2)
            self.assertEqual(session["username"], "fergalicious")
            self.assertIn("Text has been submitted!", result.data)

    def test_existing_keyword(self):
        """Test getkeyword route with an existing text in db. """

        with self.client as c:
            with c.session_transaction() as sess:
                sess["fname"]="Shakira"
                sess["user_id"]=1
                sess["username"]="shakira"
                # not working properly

            result = self.client.get("/getkeyword", 
                                    query_string={"date":"2017,3,23", "keyword":"funny", "phone":"4436668889"},
                                    follow_redirects=True)

            self.assertIn("Hi Shakira, Welcome!", result.data)                                   


    def test_texts(self):
        """Test the texts route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess["fname"]="Shakira"
                sess["user_id"]=1

            result = self.client.get("/texts")

            self.assertIn("Hey Shakira!", result.data)

    def test_get_url(self):
        """Testing the geturl route."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"]=1

            result = self.client.get("/geturl", 
                                    query_string={"url":"http://i.giphy.com/eS0vb3CoLZGuc.gif", "phone":"1231236669", "date":"2017,3,23"},
                                    )


if __name__ == '__main__':
	import unittest
	unittest.main()
    