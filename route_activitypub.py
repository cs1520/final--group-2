from flask import Response, request, jsonify, redirect, url_for

from main import app
from datastore import dao
from activitypub import ap_get_user

# Outgoing requests: (defined in activitypub.py)

# Incoming requests:
#   GET .well-known/nodeinfo    => respond with nodeinfo structure: http://nodeinfo.diaspora.software/protocol.html
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
	user_id = None
	if resource.startswith("https://"):
		# userid is always the last part of the url
		user_id = resource.split("/")[-1].split("@")[-1]
	elif resource.startswith("acct:") and resource.endswith("@pleasedontpoke.me"):
		# remove outer syntax from account id
		user_id = resource[5:-18]
	else:
		return None # not a valid resource format

	# query (internal) user in database
	user = dao.get_user(user_id)

	response = jsonify({
		"subject": f"acct:{user_id}@pleasedontpoke.me",
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

	response.headers.set("Content-Type", "application/jrd+json; charset=utf-8")
	response.headers.set("Access-Control-Allow-Origin", "*")
	return response

@app.route("/users/<user_id>", methods=["GET"])
def ap_get_user(user_id):
	accept = request.headers.get("Accept")
	# redirect to user (HTML) page if not supplied with an ActivityPub accept header
	if accept != "application/activity+json" and accept != "application/ld+json":
		return redirect(url_for("user", user_id=user_id))

	user = dao.get_user(user_id)
	response = jsonify({
		"@context": "https://www.w3.org/ns/activitystreams",
		"type": "Person",
		"id": f"https://pleasedontpoke.me/users/{user_id}",
		"inbox": f"https://pleasedontpoke.me/users/{user_id}/inbox",
		"outbox": f"https://pleasedontpoke.me/users/{user_id}/outbox",
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

	response.headers.set("Content-Type", "application/activity+json; charset=utf-8")
	return response

@app.route("/users/<user_id>", methods=["POST"])
@app.route("/users/<user_id>/inbox", methods=["POST"])
def ap_post_user(user_id):
	activity = request.get_json()
	if activity.get("type") != "Create":
		return None

	obj = activity.get("object")
	if (not obj) or obj.get("type") != "Note":
		return None

	user_to = dao.get_user(user_id)
	user_from = ap_get_user(activity.get("actor"))

	# Receive a poke from the user
	dao.create_poke(user_from["id"], user_to["id"], url=obj["id"])
	return Response(201)
