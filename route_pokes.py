from flask import render_template, request, session, jsonify
from datetime import datetime, timedelta

from main import app, render_page, get_session_user
from datastore import dao

# Pagination:
# /api/pokes?id=user -> [p1, p2, p3]
# /api/pokes?id=user&before=<p3.date> -> [p4, p5, p6]
# show more button 
# keep track of the last poke seen and append the new set of poke to them


@app.route("/api/pokes")
def query_pokes():
	"""Query pokes received before a certain date."""
	user_id = request.args.get("id")
	before_string = request.args.get("before")
	limit = request.args.get("limit")

	# Python is fun.
	limit_count = None
	if limit is not None:
		limit_count = int(limit)

	before_date = None
	if before_string is not None:
		before_date = datetime.strptime(before_string, "%a, %d %b %Y %H:%M:%S %Z")

	pokes = dao.query_pokes_sent_to(user_id, before_date=before_date, result_limit=limit_count)

	return jsonify(pokes)

@app.route("/api/pokesbetween")
def pokes_sent_between():
	"""Return the jsonified list of pokes sent from the session user to another user."""
	session_user = get_session_user()
	user_id = request.args.get("id")
	if session_user and session_user["id"] == user_id:
		pokes_between = dao.query_pokes_sent_between(session_user["id"], user_id, datetime.now() - timedelta(days=6))
		return jsonify(pokes_between)
	else:
		return None

@app.route("/api/pokesby")
def pokes_sent_by():
	"""Return the jsonified list of pokes sent by the session user."""
	session_user = get_session_user()
	user_id = request.args.get("id")
	if session_user and session_user["id"] == user_id:
		pokes_by = dao.query_pokes_sent_by(session_user["id"], datetime.now() - timedelta(days=6))
		return jsonify(pokes_by)
