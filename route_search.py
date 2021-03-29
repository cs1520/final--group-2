from flask import render_template, request, session, jsonify

from main import app, render_page
from datastore import dao

@app.route("/search")
def search():
	"""Return the results for a search query."""
	user = request.args.get('q')
	# TODO: perform intensive user search
	return render_page("search", {
		"query": request.args.get('q'),
		"users": []
	})

# /api/search/?q=username
@app.route("/api/search")
def search_json():
	"""Return search results as a JSON array"""
	query = request.args.get("q")
	users = dao.query_users(query)

	# Only return "id" and "name" keys
	result_users = list(map(lambda user: {
		"id": user['id'],
		"name": user['name']
	}, users))

	return jsonify(result_users)