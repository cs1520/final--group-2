from flask import render_template, request, session, jsonify, url_for, redirect

from main import app, render_page, get_session_user
from datastore import dao
from activitypub import ap_get_user

@app.route("/search")
def search():
	"""
	Return the results for a search query.
	If no matching users are found, will check if such an ActivityPub user exists.
	If an ActivityPub user exists, return their profile page.
	"""
	if get_session_user() is None:
		return redirect(url_for("login"))

	query = request.args.get('q')
	users = dao.query_users(query)

	if not users:
		try: # search for a remote user if possible
			remote_user = ap_get_user(query)
			users = [remote_user] if remote_user else []
		except:
			"do nothing"

	result_users = list(map(lambda user: {
		"id": user["id"],
		"name": user["name"],
		"image": user["image"]
	}, users))

	return render_page("search.html", {
		"query": request.args.get('q'),
		"users": result_users
	})

# /api/search/?q=username
@app.route("/api/search")
def search_json():
	"""Return search results as a JSON array"""
	if get_session_user() is None:
		return None

	query = request.args.get("q")
	users = dao.query_users(query)

	if not users:
		try: # search for a remote user if possible
			remote_user = ap_get_user(query)
			users = [remote_user] if remote_user else []
		except:
			"do nothing"

	# Only return "id" and "name" keys
	result_users = list(map(lambda user: {
		"id": user['id'],
		"name": user['name']
	}, users))

	return jsonify(result_users)
