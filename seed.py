""" Utility file to seed texts database from (u.user/u.text) seed_data """
from sqlalchemy import func
from model import User
from model import Text
from model import connect_to_db, db
from server import app
from datetime import datetime


def load_users():
    """Load users from user.data into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read users.data file and insert data
    for row in open("seed_data/u.user"):

        row = row.rstrip()

        user_id, fname, lname, username, password = row.split("|")

        user = User(user_id=user_id,
                    fname=fname,
                    lname=lname,
                    username=username,
                    password=password)

        db.session.add(user)

    db.session.commit()
    print "Users"


def load_texts():
    """Load texts from u.data into database."""

    Text.query.delete()

    for row in open("seed_data/u.text"):

        # removes all the extra white space from the rows and splits at the pipe (makes a list)
        row = row.rstrip().split("|")

        # I was getting this ("ValueError: too many values to unpack") so i slice the unpacking into 2.
        text_id, user_id, keyword= row[0:3]
        phone, url, send_out_date, sent = row[3:]

        text = Text(text_id=text_id, user_id=user_id, keyword=keyword, phone=phone,
                    url=url, send_out_date=send_out_date, sent=sent)

        # need to have "add" to the session or it won't ever be stored
        db.session.add(text)

    # this will commit it
    db.session.commit()
    print "Texts"


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_text_id():
    """Set value for the next text_id after seeding database"""

    # Get the Max text_id in the database
    result = db.session.query(func.max(Text.text_id)).one()
    max_id = int(result[0])

    # Set the value for the next text_id to be max_id + 1
    query = "SELECT setval('texts_text_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()    


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_texts()
    set_val_user_id()
    set_val_text_id()
