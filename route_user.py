from flask import render_template, request, redirect, url_for, jsonify

from main import app, get_session_user, render_page
from datastore import dao
from storage import upload_file

from datetime import datetime, timedelta

@app.route("/@<user_id>", methods=["POST", "GET"])
def user(user_id):
	"""Return, and potentially poke, the user profile page."""
	session_user = get_session_user()
	user = session_user
	my_pokes_to = None
	pokes = None
	was_poked = False

	# if the user is looking at their own profile...
	if session_user and session_user["id"] == user_id:
		# get all poke interactions sent from session_user to anyone
		my_pokes_to = dao.query_pokes_sent_by(session_user["id"])
	else:
		user = dao.get_user(user_id)
		# if method=POST, poke the user
		if request.method == "POST":
			dao.create_poke(session_user["id"], user["id"])
			was_poked = True
		# get all poke interactions sent from session_user to user
		if session_user is not None:
			my_pokes_to = dao.query_pokes_sent_between(session_user["id"], user["id"])

	# get all pokes sent to the given user
	pokes = user["pokes"]

	return render_page("user.html", {
		"user": user,
		"pokes": pokes,
		"sent_pokes": my_pokes_to,
		"was_poked": was_poked
	})

@app.route("/@<user_id>/edit", methods=["GET", "POST"])
def user_edit(user_id):
	"""Return the editor interface for the user profile page."""
	session_user = get_session_user()

	if session_user is None or session_user["id"] != user_id:
		return redirect(url_for("user", user_id=user_id))

	# if method=POST, update the user entry
	if request.method == "POST":
		user_edit = {
			"id": user_id,
			"name": request.form.get("name") or session_user["name"],
			"bio": request.form.get("bio") or session_user["bio"]
		}

		# upload new profile image (if provided)
		user_image = request.files.get("image")
		if user_image:
			user_edit["image"] = upload_file(user_image)

		# update user info & return
		dao.update_user(user_edit)
		return redirect(url_for("user", user_id=user_id))

	# otherwise, return the user edit page
	user = dao.get_user(user_id)
	return render_page("user-edit.html", {
		"user": user
	})
