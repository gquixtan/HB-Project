""" Models for texts db. """
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from datetime import datetime
from flask import Flask

db = SQLAlchemy()


class User(db.Model):
    """User model."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(123), nullable=False)
    lname = db.Column(db.String(123), nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String(123), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s fname=%s lname=%s username%s>" % (self.user_id,
                                                                   self.fname,
                                                                   self.lname,
                                                                   self.username)


class Text(db.Model):
    """Text model."""

    __tablename__ = "texts"

    text_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    keyword = db.Column(db.String(123), nullable=True)
    phone = db.Column(db.String(10), nullable=False)
    url = db.Column(db.Text, nullable=True)
    send_out_date = db.Column(db.DateTime, nullable=False)
    sent = db.Column(db.Boolean, nullable=True, default=False)

    # Define relationship to user
    user = db.relationship("User", backref="texts")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Text text_id=%s user_id=%s keyword=%s phone=%s url=%s send_out_date=%s sent=%s>" % (self.text_id,
                                                                                                              self.user_id,
                                                                                                              self.keyword,
                                                                                                              self.phone,
                                                                                                              self.url,
                                                                                                              self.send_out_date,
                                                                                                              self.sent)


def test_texts():
    """Create sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Text.query.delete()

    Shakira = User(fname="Shakira",lname="Ripoll", username="shakira", password="123go")
    Fergie = User(fname="Fergie", lname="Licious", username="fergalicious", password="123go")

    Cat = Text(keyword="funny", phone="4436668889", send_out_date="2017,3,23", sent="t")
    Dance= Text(keyword="dance", phone="4436668889", send_out_date="2017,3,23", sent="t")

    db.session.add_all([Shakira, Fergie, Cat, Dance])
    db.session.commit()    


def connect_to_db(app, db_uri="postgresql:///texts"):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # from flask import Flask
    from server import app
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."

    db.create_all()

