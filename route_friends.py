from flask import render_template, request, session, redirect, url_for

from main import app, get_session_user, render_page
from datastore import dao

@app.route("/friends")
def friends():
	"""Return the user's friends list."""
	user = get_session_user()
	user_friends = list(map(
		lambda user_id: dao.get_user(user_id),
		user["friends"]
	))

	return render_page("friends.html", {
		"friends": user_friends,
	})
