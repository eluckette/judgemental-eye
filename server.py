"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


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
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/user-homepage')
def user_homepage():
    return "test"
    #return render_template('user.html')
    #get ratings and movie titles from user object


@app.route('/login')
def login():
    """Login form"""

    return render_template('login_form.html')

@app.route('/login-submission', methods=['POST'])
def handle_login():
    """Handles the login form and adds the user to the session."""

    user = User.query.filter_by(email=request.form['username']).first()
 
    if user and (user.password == request.form['password']):
        session['username'] = user.email
        flash("Login successful!")
        return render_template('homepage.html')
        #return redirect('/user-homepage', DEBUG_TB_INTERCEPT_REDIRECTS=False)
    else:
        flash("Invalid login.")
        return render_template('login_form.html')

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

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()