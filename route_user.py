from flask import render_template, request

from main import app, get_session_user, render_page
from datastore import dao

@app.route("/@<user>", methods=["POST", "GET", "PUT"])
def user(user_id):
	"""Return, and potentially poke, the user profile page."""
	session_user = get_session_user()

	if session_user and session_user["id"] == user_id:
		if request.method == "PUT":
			"TODO: dao.update_user"

		my_sent_pokes = dao.query_pokes_sent_by(session_user)
		return render_page("user.html", {
			"user": session_user,
			"pokes": my_sent_pokes
		})
	else:
		other_user = dao.get_user(user_id)
		if request.method == "POST":
			dao.create_poke(session_user, other_user)

		sent_pokes = None
		if session_user is not None:
			sent_pokes = dao.query_poke_sent_between(session_user, other_user)

		return render_page("user.html", {
			"user": user,
			"pokes_between": sent_pokes
		})
