from flask import Flask, request, render_template
import urllib
import json

# from random import choice, sample
# import os
# import giphy


app = Flask(__name__)


@app.route("/")
def index():
    """Return homepage."""

    return render_template("index.html")


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