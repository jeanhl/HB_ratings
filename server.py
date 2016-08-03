"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import User, Rating, Movie, connect_to_db, db
from flask_debugtoolbar import DebugToolbarExtension



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/register", methods=['GET'])
def register_form():

    return render_template("register_form.html")


@app.route("/register", methods=['POST'])
def register_process():

    return redirect("/")


@app.route('/login', methods=['POST'])
def login_form():
    """Processes login form."""

    username = request.form.get("username")
    password = request.form.get("password")

    isUser = User.query.filter_by(email=username).all()

    session[isUser[0].email] = isUser[0].password

    if isUser[0].email == username and isUser[0].password == password:
        flash("Logged In !!!!!")
        return redirect("/")
    else:
        flash("Email / Password doesn't match. Try again.")
        return redirect("/")

@app.route('/logout', methods=['POST'])
def logout_form():
    """Processes logout form."""

    for key, item in session:
        del session[key]

    return redirect("/")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template('user_list.html', users=users)





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

