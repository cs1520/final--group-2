from flask import Flask, redirect, url_for, render_template, request, session

from datastore import dao

app = Flask(__name__)
app.secret_key = b'oaijrwoizsdfmnvoiajw34foinmzsdv98j234'

# Get the user of the current session id
def get_session_user():
	if session.get('user') is None:
		return

	user = dao.get_user(session['user'])
	return user

# Render a page for the current user
def render_page(template, options={}):
	session_user = get_session_user()
	return render_template(template,
		page = options,
		user = session_user)

import route_login
import route_home
import route_notifications
import route_search
import route_user
import route_pokes
import route_friends
import route_activitypub

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
