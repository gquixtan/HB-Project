from flask import Flask, request, render_template, redirect
import urllib
import json
import twilio_text


app = Flask(__name__)


@app.route("/")
def index():
    """Return homepage."""

    return render_template("index.html")


@app.route("/login")
def login():
    """ login the user """

    return render_template("login.html")


@app.route("/register")
def register():
    """ create new user """

    return render_template("register.html")


@app.route("/sendtext")
def get_keyword():
    """ """

    keyword = request.args.get("keyword")

    twilio_text.send_text(keyword)
    # test = twilio_text.send_text(keyword)
    # print test

    # flash("Message has been submitted!")

    return redirect("/profile")


@app.route("/profile")
def say_hello():
    """Simple profile page."""

    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

    # app.run(port=5000, host='0.0.0.0')

    # app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)