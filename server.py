from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
# import json
import twilio_text
# from datetime import datetime
from model import connect_to_db, db, User, Text


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "123go"

app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("index.html")


@app.route("/login", methods=["GET"])
def login():
    """log in the user """

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_process():
    """ Check if the user is in the db and log them in to their profile """

    # get the username and password from the user through the form
    username = request.form.get('username')
    password = request.form.get('password')


    # this query checks if user is in the database
    user = db.session.query(User).filter(User.username == username,
                                         User.password == password).first()
    # print user



    # if the user in not registered redirect them to register
    if user is None:
        return redirect("/register")
    # if the is in the db redirect them to their profile and flashed them a succeful logged in msg
    else:
        # flash('You were successfully logged in')
        session['username'] = user.username
        session['user_id'] = user.user_id
        session['fname'] = user.fname
        fname = session['fname']

        flash('You were successfully logged in')
        return redirect("/profile")


@app.route("/register", methods=["GET"])
def register():
    """ create new user """

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_form():
    """Register a new user"""


    # get the username, fname, lname and password from the user through the form
    fname = request.form.get('firstname')
    lname = request.form.get('lasttname')
    username= request.form.get('username')
    password= request.form.get('password')


    # query to see if user is in db
    user = db.session.query(User).filter(User.password == password, 
                                        User.username == username, 
                                        User.fname == fname,
                                        User.lname == lname).first()

    # if user is not in the database, add user to database
    if user is None:
        user = User(username=username, password=password, lname=lname, fname=fname)
        db.session.add(user)
        db.session.commit()
    else:
        return redirect("/login")

    return redirect("/login")    


@app.route("/sendtext")
def text_form():
    """ """

    user_id = session['user_id']
    keyword = request.args.get("keyword")
    send_out_date = request.args.get("date")
    phone = request.args.get("phone")
    msg = request.args.get("msg")



    text = db.session.query(Text).filter(Text.user_id == user_id, Text.phone == phone, 
                                        Text.send_out_date == send_out_date, 
                                        Text.keyword == keyword, Text.msg == msg).first()
    # print text


    if text is None:
        text = Text(user_id=user_id, keyword=keyword, phone=phone, msg=msg, send_out_date=send_out_date)
        db.session.add(text)
        db.session.commit()
        flash("Message has been submitted!")
        return redirect("/profile")

    return redirect("/profile")            


    # this is for twilio/giphy set up
    # twilio_text.send_text(keyword)
    # test = twilio_text.send_text(keyword)
    # print test

    # flash("Message has been submitted!")

    # return redirect("/profile")


@app.route("/profile")
def say_hello():
    """Simple profile page."""

    return render_template("profile.html", username=session['username'], fname=session['fname'])

@app.route('/logout')
def log_out():
    """ route to log """ 
    # print session['person']
    
    if 'person' in session:
        del session['person']
        
    else:
        print "Youn need to sign in" 
        # flash("Youn need to sign in")
    # flash('You were successfully logged out')    
    return redirect('/')


if __name__ == "__main__":

    # app.run(port=5000, host='0.0.0.0')

    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(debug=True, host='0.0.0.0')
