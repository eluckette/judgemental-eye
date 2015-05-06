"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

from sqlalchemy import update

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')

@app.route("/users")
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/user/<int:user_id>')
def show_user(user_id):
    """Show user"""

    user = User.query.get(user_id)
    return render_template('user.html', user=user)

@app.route('/movies')
def movie_list():
    """Show list of movies"""

    movies = Movie.query.order_by(Movie.title).all()
    return render_template('movie_list.html', movies=movies)

@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def show_movie(movie_id):
    """Show movie"""
    
    rating_status = Rating.query.filter_by(user_id=session['username'], movie_id=movie_id).first()
    movie = Movie.query.get(movie_id)

    if request.method == 'GET':
        
        return render_template('movie.html', movie=movie, rating_status=rating_status)

    else:

        user_rating = request.form['user_rating']
            
        if rating_status:
            rating_status.score = user_rating

        else:
            rating_status = Rating(user_id=session['username'], movie_id=movie_id, score=user_rating)
            db.session.add(rating_status)
            
        db.session.commit()        
        return render_template('movie.html', movie=movie, rating_status=rating_status)

@app.route('/login')
def login():
    """Login form"""

    return render_template('login_form.html')

@app.route('/login-submission', methods=['POST'])
def handle_login():
    """Handles the login form and adds the user to the session."""

    user = User.query.filter_by(email=request.form['username']).first()

    if not user:
        return render_template('register.html')
    else:
        if user and (user.password == request.form['password']):
            session['username'] = user.user_id
            flash("Login successful!")
            return redirect('/user/' + str(user.user_id))
        else:
            flash("Invalid login.")
            return render_template('login_form.html')

@app.route('/registration-submission', methods=['POST'])
def handle_registration():
    """Handles the registration form and adds the user to DB and session."""

    username = request.form['username']
    password = request.form['password']
    reenter_password = request.form['reenter_password']
    age = request.form['age']
    zipcode = request.form['zipcode']

    if password == reenter_password:
        user = User(email=username, password=password, age=age, zipcode=zipcode)
        session['username'] = user.user_id
        
        db.session.add(user)
        db.session.commit()

        return redirect('/user/' + str(user.user_id))
    else:
        flash("Passwords do not match, try again.")
        return render_template('register.html')

@app.route('/log-out')
def log_out():
    """Logs user out and removes user from the session."""

    del session['username']
    flash("Logged out.")

    return render_template('login_form.html')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()