from flask import render_template, request, jsonify, redirect, url_for

from main import app
from datastore import dao
from activitypub import ap_get_user

# Outgoing requests: (defined in activitypub.py)

# Incoming requests:
#   GET .well-known/webfinger   => respond with webfinger structure for profile links
#   GET @user with 'application/activitypub+json' or 'application/ld+json' Accept header
#                               => respond with ActivityPub structure for profile info
#   POST @user with Note object (incoming message) https://www.w3.org/TR/activitypub/#create-activity-outbox
#                               => interpret as poke & add corresponding Poke object to db

@app.route("/.well-known/webfinger")
def ap_webfinger():
	"""
	Provide user info to other ActivityPub implementations
	"""

	resource = request.args.get("resource")
	if not resource.startswith("acct:"):
		return None # anything other than accounts are not supported
	if not resource.endswith("@pleasedontpoke.me"):
		return None # cannot be used to query external users

	# remove outer syntax and query (internal) user in database
	user_id = resource[5:-18]
	user = dao.get_user(user_id)

	return jsonify({
		"subject": f"acct:{user_id}",
		"aliases": [
			f"https://pleasedontpoke.me/@{user_id}",
			f"https://pleasedontpoke.me/users/{user_id}"
		],
		"links": [{
			"rel": "http://webfinger.net/rel/profile-page",
			"type": "text/html",
			"href": f"https://pleasedontpoke.me/@{user_id}"
		},{
			"rel": "self",
			"type": "application/activity+json",
			"href": f"https://pleasedontpoke.me/users/{user_id}"
		}]
	})

@app.route("/users/<user_id>", methods=["GET"])
def ap_get_user(user_id):
	accept = request.headers.get("Accept")
	# redirect to user (HTML) page if not supplied with an ActivityPub accept header
	if accept != "application/activity+json" and accept != "application/ld+json":
		return redirect(url_for("user", user_id=user_id))

	user = dao.get_user(user_id)
	return jsonify({
		"@context": "https://www.w3.org/ns/activitystreams",
		"id": f"https://pleasedontpoke.me/users/{user_id}",
		"type": "Person",
		"preferredUsername": user_id,
		"name": user["name"],
		"summary": user["bio"],
		"url": f"https://pleasedontpoke.me/@{user_id}",
		"discoverable": True,
		"icon": {
			"type": "Image",
			"mediaType": "image/png",
			"url": user["image"]
		}
	})

@app.route("/users/<user_id>", methods=["POST"])
def ap_post_user(user_id):
	activity = request.get_json()
	if activity.get("type") != "Create":
		return None

	obj = activity.get("object")
	if obj.get("type") != "Note":
		return None

	user_to = dao.get_user(user_id)
	user_from = ap_get_user(activity.get("actor"))

	# Receive a poke from the user
	dao.create_poke(user_from["id"], user_to["id"], url=obj["id"])
