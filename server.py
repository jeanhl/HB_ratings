"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, url_for)

from model import User, Rating, Movie, connect_to_db, db
# from seed import manual_load_user
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


@app.route("/go_to_register")
def register_page():
    """ Registers users. """

    return render_template("register_form.html")


@app.route("/register", methods=['POST'])
def register_form():
    """ Registers users. """
    
    r_email = request.form.get('r_email') 
    r_age = request.form.get('r_age')
    r_zipcode = request.form.get('r_zipcode') 
    r_password = request.form.get('r_password')


    user = User(email=r_email,
                age=r_age,
                zipcode=r_zipcode,
                password=r_password)

        # We need to add to the session or it won't ever be stored
    db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()
    flash("Welcome to Judgemental Eye, new user!")

    return redirect("/")


@app.route('/login', methods=['POST'])
def login_form():
    """Processes login form."""

    username = request.form.get("username")
    password = request.form.get("password")

    user_object = User.query.filter_by(email=username).first()

    if user_object.email == username and user_object.password == password:
        flash("Logged In !!!!!")
        session["user_email"] = user_object.email
        session["user_id"] = user_object.user_id
        user_id = user_object.user_id
        return redirect(url_for('user_details', user_id=user_id))
    else:
        flash("Email / Password doesn't match. Try again.")
        return redirect("/")


@app.route('/logout', methods=['POST'])
def logout_form():
    """Processes logout form."""

    session.clear()

    flash("Logged out. Come back soon!")

    return redirect("/")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template('user_list.html', users=users)



@app.route('/user_details/<user_id>')
def user_details(user_id):
    """Show user details"""

    users = User.query.filter_by(user_id=user_id).first()
    # rating = Rating.query.filter_by(user_id=user_id).all()
    # movies = Rating.query.join(Movie, Rating.movie_id==Movie.movie_id).filter_by(Rating.user_id=user_id).all()

    all_rating_details = Rating.query.filter_by(user_id=user_id).all()
    movie_list = []
    for each_detail in all_rating_details:
        movie_all = Movie.query.filter_by(movie_id=each_detail.movie_id).all()
        score_movie = (each_detail.score, movie_all[0].title)
        movie_list.append(score_movie)

    return render_template ("user_details.html", users=users, movie_list=movie_list)

@app.route('/movies')
def movie_list():
    """ Show alphabetical list of movies """

    all_movies = Movie.query.order_by(Movie.title)

    return render_template('movies.html', all_movies=all_movies)


@app.route('/movie_details/<movie_id>')
def movie_details(movie_id):

    movie_details = Movie.query.filter_by(movie_id=movie_id)
    movie_rating =  Rating.query.filter_by(movie_id=movie_id)

    return render_template('movies_details.html', 
                            movie_details=movie_details,
                            movie_rating=movie_rating )


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

