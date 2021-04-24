from flask import render_template, request, session, jsonify, redirect, url_for

from main import app, render_page, get_session_user
from datastore import dao

@app.route("/notifications")
def notifications():
	"""Return the user's recent pokes."""
	if get_session_user() is None:
		return redirect(url_for("login"))
	return render_page("notifications.html", { "pokes": [] })
