from flask import render_template, request, session, jsonify

from main import app, render_page
from datastore import dao

@app.route("/notifications")
def notifications():
	"""Return the user's recent pokes."""
	return render_page("notifications.html", { "pokes": [] })
