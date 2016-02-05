"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register')
def register_user():
	"""Allow user to register."""

	return render_template('registration-form.html')


@app.route('/registered', methods=["POST"])
def add_user_to_db():
	"""Add new user to table users."""

	# Get form values
	form_email = request.form.get("email")
	form_password = request.form.get("password")
	form_age = request.form.get("age")
	form_zipcode = request.form.get("zipcode")

	# Validate age field:
	if form_age:
		form_age = int(form_age)
	elif form_age == "":
		form_age = None

	# Validate zipcode field:
	if form_zipcode == "":
		form_zipcode = None

	# Instantiate new User object based on form values
	new_user = User(email=form_email, password=form_password, 
					age=form_age, zipcode=form_zipcode)

	# Add new User to db
	db.session.add(new_user)
	db.session.commit()

	# Redirect to homepage and confirm registration
	flash("You've successfully registered!")
	return redirect("/")


@app.route('/sign-in')
def sign_in():
	"""Sign-in user."""

	return render_template("sign-in_form.html")


@app.route('/signed-in', methods=["POST"])
def check_user_existence():
	"""Allow user to login given correct credentials."""

	# Get form values
	form_email = request.form.get("email")
	form_password = request.form.get("password")

	# Get user object whose email matches form's email
	user = User.query.filter(User.email == form_email).first()

	# If email and password combo matches, logs in successfully
	if user and user.password == form_password:
		session["user_id"] = user.user_id
		flash("You've successfully logged in!")
		return redirect("/")

	elif not user or user.password != form_password:
		flash("Invalid email or password. Please register if you do not have an account.")
		return redirect("/sign-in")


@app.route('/users')
def user_list():
	"""Show list of users."""

	# Get list of User objects
	users = User.query.all()

	return render_template("user_list.html", users=users)


@app.route('/users/<int:user_id>')
def user_page(user_id):
	"""Show page for user."""

	# Given user_id, get User object
	user = User.query.filter(User.user_id == user_id).first()
	
	# Get list of movie-score tuples
	movies_scores = db.session.query(Movie.title, Rating.score).join(Rating).filter(Rating.user_id == 1).order_by(Movie.title).all()

	return render_template("user-page.html", user=user, movies_scores=movies_scores)


@app.route('/movies')
def movie_list():
	"""Show list of movies."""

	# Get list of Movie objects
	movies = Movie.query.order_by("title").all()

	return render_template("movie_list.html", movies=movies)


@app.route('/movies/<int:movie_id>')
def movie_page(movie_id):
	"""Show page for movie."""

	# If user not logged in:
	if not session.get('user_id'):
		# Given movie_id, get Movie object
		movie = Movie.query.filter(Movie.movie_id == movie_id).first()

		# Get list of rating tuples
		ratings = db.session.query(Rating.score).filter(Rating.movie_id == movie_id).all()

		return render_template("movie-page.html", movie=movie, ratings=ratings)

	# If user logged in:
	else:
		# Given movie_id, get Movie object
		movie = Movie.query.filter(Movie.movie_id == movie_id).first()

		# Get list of rating tuples
		ratings = db.session.query(Rating.score).filter(Rating.movie_id == movie_id).all()

		return render_template("movie-page-logged-in.html", movie=movie, ratings=ratings)


@app.route('/movies/<int:movie_id>/rated', methods=['GET'])
def rate_movie(movie_id):
	"""Add new rating to table ratings."""

	# Get form values
	movie_id = movie_id
	user_id = session.get('user_id')
	score = request.args.get("score")


	# Instantiate new Rating object
	rating = Rating(movie_id=movie_id, user_id=user_id, score=score)

	print rating, "**********************************************************"

	# Add new Rating to db
	db.session.add(rating)
	db.session.commit()

	# Redirect to movie page and confirm rating submission
	flash("Your rating has been added!")
	return redirect("/movies/<int:movie_id>")


@app.route('/log-out')
def logout():
	"""Logout user."""

	if session.get("user_id"):
		del session["user_id"]
		flash("You've successfully logged out!")
	
	return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()







# First attempt at adding new users and handling login/logout

# # Making a list of email tuples from user table
# 	QUERY = "SELECT email FROM users"
# 	cursor = db.session.execute(QUERY)
# 	emails = cursor.fetchall()

# 	email_list = []
# 	emails_length = len(emails)
# 	print emails_length, "---------------------------------------"
# 	counter = 0

# 	# Encode each email in table list of tuples and add to empty email_list
# 	while counter != emails_length:
# 		if not email_list:	# If email_list is empty
# 			current_email = emails[0][0].encode('utf-8')
# 			email_list.append(current_email)
# 			counter += 1
# 			print email_list
# 		elif email_list:	# Else, if email_list is not empty
# 			for email in emails[1:]:
# 				current_email = email[0].encode('utf-8')
# 				email_list.append(current_email)
# 				counter += 1

# 	print email_list, "*************************"

# 	# If email is not in the email list, then we insert new user into table
# 	if form_email not in email_list:
# 		QUERY = "INSERT INTO users (email, password) VALUES (:email, :password)"
# 		db.session.execute(QUERY, {'email': form_email, 'password': form_password})
# 		db.session.commit()
# 		return redirect("/")

# 	else:
# 		QUERY = "SELECT password FROM users WHERE email = :email"
# 		password = db.session.execute(QUERY, {'email': form_email}).fetchone()
# 		if form_password == password:
# 			return redirect("/")
# 		else:
# 			return redirect("/")
# 		# else:
# 			# use JS to prevent form submission