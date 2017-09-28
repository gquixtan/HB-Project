""" Models for msgs db. """
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from datetime import datetime
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User model."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(69), nullable=False)
    lname = db.Column(db.String(69), nullable=False)
    password = db.Column(db.String(69), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s fname=%s lname=%s>" % (self.user_id, self.fname,
                                                                self.lname)

class Text(db.Model):
    """Text model."""

    __tablename__ = "txts"

    text_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    giphy_keyword = db.Column(db.String(69), nullable=True)
    phone = db.Column(db.String(12), nullable=True)
    msg_descirption = db.Column(db.Text, nullable=False)
    send_out_date = db.Column(db.DateTime, nullable=True)
    # creation_date = db.Column(db.DateTime, nullable=False)


    # Define relationship to user
    user = db.relationship("Text", backref=db.backref("users"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Text text_id=%s user_id=%s giphy_keyword=%s phone=%s msg_descirption=%s send_out_date=%s >" % (self.text_id,
                                                                                              self.user_id,
                                                                                              self.giphy_keyword,
                                                                                              self.phone,
                                                                                              self.msg_descirption,
                                                                                              self.send_out_date)


def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///msgs'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    # db.create_all()
    # db.session.commit()

if __name__ == "__main__":
    # from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."
