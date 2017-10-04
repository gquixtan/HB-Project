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
    keyword = db.Column(db.String(123), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    msg = db.Column(db.Text, nullable=True)
    send_out_date = db.Column(db.DateTime, nullable=False)

    # Define relationship to user
    user = db.relationship("User", backref="texts")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Text text_id=%s user_id=%s keyword=%s phone=%s msg=%s send_out_date=%s >" % (self.text_id,
                                                                                                              self.user_id,
                                                                                                              self.keyword,
                                                                                                              self.phone,
                                                                                                              self.msg,
                                                                                                              self.send_out_date)



# add a column sent (t/f)?
# creation_date = db.Column(db.DateTime, nullable=True, default=None) ??? 

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///texts'
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

