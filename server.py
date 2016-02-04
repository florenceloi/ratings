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


@app.route('/users')
def user_list():
	"""Show list of users."""

	users = User.query.all()

	return render_template("user_list.html", users=users)

@app.route('/sign-in')
def sign_in():
	"""Sign-in user."""

	return render_template("sign-in_form.html")

@app.route('/signed-in', methods=["POST"])
def check_user_existence():
	"""Check to see if user is in database, and if not, create user."""

	# get username from form
	form_email = request.form.get("email")
	# get password from form
	form_password = request.form.get("password")

	# get user object whose email matches form's email
	user = User.query.filter(User.email == form_email).first()

	# if email and password combo matches, logs in successfully
	if user and user.password == form_password:
		
		
		flash("You've successfully logged in!")
		return redirect("/")

	elif not user or user.password != form_password:
		flash("Invalid email or password. Please register if you do not have an account.")
		return redirect("/sign-in")

	
	else:
		return redirect("/sign-in")






	# # Making a list of email tuples from user table
	# QUERY = "SELECT email FROM users"
	# cursor = db.session.execute(QUERY)
	# emails = cursor.fetchall()

	# email_list = []
	# emails_length = len(emails)
	# print emails_length, "---------------------------------------"
	# counter = 0

	# # Encode each email in table list of tuples and add to empty email_list
	# while counter != emails_length:
	# 	if not email_list:	# If email_list is empty
	# 		current_email = emails[0][0].encode('utf-8')
	# 		email_list.append(current_email)
	# 		counter += 1
	# 		print email_list
	# 	elif email_list:	# Else, if email_list is not empty
	# 		for email in emails[1:]:
	# 			current_email = email[0].encode('utf-8')
	# 			email_list.append(current_email)
	# 			counter += 1

	# print email_list, "*************************"

	# # If email is not in the email list, then we insert new user into table
	# if form_email not in email_list:
	# 	QUERY = "INSERT INTO users (email, password) VALUES (:email, :password)"
	# 	db.session.execute(QUERY, {'email': form_email, 'password': form_password})
	# 	db.session.commit()
	# 	return redirect("/")

	# else:
	# 	QUERY = "SELECT password FROM users WHERE email = :email"
	# 	password = db.session.execute(QUERY, {'email': form_email}).fetchone()
	# 	if form_password == password:
	# 		return redirect("/")
	# 	else:
	# 		return redirect("/")
	# 	# else:
	# 		# use JS to prevent form submission


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