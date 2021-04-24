from flask import render_template, request, session, jsonify, redirect, url_for
from datetime import datetime, timedelta

from main import app, render_page, get_session_user
from datastore import dao

import random

@app.route("/")
def home():
	"""Return the user's home page."""
	if get_session_user() is None:
		return redirect(url_for("login"))
	else:
		return suggest()

def suggest(suggestion_count=6):
	"""Suggest people for the session user to poke."""
	user = get_session_user()

	suggestion_entities = set()
	if user:
		suggestions = set()
		recent_pokes = dao.query_recent_pokes()
		for poke in recent_pokes:
			if poke["poker"] not in user["friends"] and poke["poker"] != user["id"]:
				suggestions.add(poke["poker"])
			if poke["pokee"] not in user["friends"] and poke["pokee"] != user["id"]:
				suggestions.add(poke["pokee"])
			if len(suggestions) >= suggestion_count:
				break
		suggestion_entities = list(map(
			lambda user_id: dao.get_user(user_id),
			suggestions
		))

	return render_page("index.html", {
		"suggestions": suggestion_entities
	})
