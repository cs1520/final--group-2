from hashlib import sha256
from uuid import uuid4
from hmac import compare_digest
from Cryptodome.PublicKey import RSA
from flask import render_template, request, session, redirect, url_for

from main import app
from datastore import dao

import re

matcher = re.compile('[a-zA-Z0-9_]+')

def create_password_hash(password, salt):
	sha = sha256(password.encode('utf-8') + salt.encode('utf-8'))
	return sha.hexdigest()

# Show the login page
@app.route("/login")
@app.route("/register")
def show_login():
	return render_template("login.html", page = {})

# Create a new user account
@app.route("/register", methods=["POST"])
def register():
	username = request.form.get("username")
	password = request.form.get("password")
	password_confirm = request.form.get("password-confirm")

	if len(username) <= 0:
		return render_template("login.html", page = { "error": "Username must be an ASCII string of nonzero length." })

	if not matcher.match(username):
		return render_template("login.html", page = { "error": "Username must only contain alphanumeric characters, with the exception of underscores." })

	if len(password) <= 0 or password != password_confirm:
		return render_template("login.html", page = { "error": "Passwords must match!" })

	if dao.get_user(username) is not None:
		return render_template("login.html", page = { "error": "Your username must be unique!" })

	if len(username) > 15:
		return render_template("login.html", page = { "error": "Your username must be 15 or fewer characters long."})

	# create the hashed/salted password values
	password_salt = uuid4().hex
	password_hash = create_password_hash(password, password_salt)

	# generate a pub/priv RSA keypair (for ActivityPub)
	rsa_privkey = RSA.generate(2048)
	rsa_pubkey = rsa_privkey.publickey()

	# add the new user to datastore
	user = dao.create_user(
		username,
		rsa_privkey=rsa_privkey.export_key("PEM").decode("utf-8"),
		rsa_pubkey=rsa_pubkey.export_key("PEM").decode("utf-8"),
		password=password_hash,
		salt=password_salt
	)

	# set the user session variable
	session['user'] = user['id']
	return redirect(url_for('home'))

# Authenticate an existing user
@app.route("/login", methods=["POST"])
def login():
	username = request.form.get("username")
	password = request.form.get("password")

	if len(username) <= 0:
		return render_template("login.html", page = { "error": "Username must be an ASCII string of nonzero length." })

	if len(password) <= 0:
		return render_template("login.html", page = { "error": "Password field cannot be empty."})

	# get user from db
	user = dao.get_user(username)
	if user is None or len(user["password"]) <= 0:
		return render_template("login.html", page = { "error": "User does not exist!" })

	# compare / verify the provided password hash
	password_hash = create_password_hash(password, user['salt'])
	if not compare_digest(user["password"], password_hash):
		return render_template("login.html", page = { "error": "Incorrect username or password!" })

	# add user session & redirect
	session['user'] = user['id']
	return redirect(url_for('home'))

@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('login'))
