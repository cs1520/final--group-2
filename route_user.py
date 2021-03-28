from flask import render_template, request, redirect, url_for

from main import app, get_session_user, render_page
from datastore import dao
from storage import upload_file

@app.route("/@<user_id>", methods=["POST", "GET"])
def user(user_id):
	"""Return, and potentially poke, the user profile page."""
	session_user = get_session_user()
	user = session_user
	pokes = None

	# if the user is looking at their own profile...
	if session_user and session_user["id"] == user_id:
		# set the pokes list to all interactions sent from the current user
		pokes = dao.query_pokes_sent_by(session_user['id'])
	else:
		user = dao.get_user(user_id)
		# if method=POST, poke the user
		if request.method == "POST":
			dao.create_poke(session_user['id'], user['id'])
		# set the pokes list to all interactions between the two users
		if session_user is not None:
			pokes = dao.query_pokes_sent_between(session_user['id'], user['id'])

	return render_page("user.html", {
		"user": session_user,
		"pokes": pokes
	})

@app.route("/@<user_id>/edit", methods=["GET", "POST"])
def user_edit(user_id):
	"""Return the editor interface for the user profile page."""
	session_user = get_session_user()

	if session_user is None or session_user["id"] != user_id:
		return redirect(url_for('user', user_id=user_id))

	# if method=POST, update the user entry
	if request.method == "POST":
		user_edit = {
			"id": user_id,
			"name": request.form.get("name"),
			"bio": request.form.get("bio")
		}

		# upload new profile image (if provided)
		user_image = request.files.get("image")
		if user_image:
			user_edit["image"] = upload_file(user_image)

		# update user info & return
		dao.update_user(user_edit)
		return redirect(url_for('user', user_id=user_id))

	# otherwise, return the user edit page
	user = dao.get_user(user_id)
	return render_page("user-edit.html", {
		"user": user
	})
