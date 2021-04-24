from flask import render_template, request, session, jsonify
from requests import get, post

from main import app, render_page
from datastore import dao

from datetime import datetime, timedelta
from activipy import vocab

# Outgoing requests:
#   search for user@example.com => query example.com & add new (discovered) user info to db
#   poke user@example.com       => send a Note to example.com & increment database poke count for user

# Incoming requests: (implemented in route_activitypub.py)

def ap_get_links(user_str):
	"""
	Fetch user info using Webfinger based on formatting (http://domain/user, user@domain, etc.)
	"""

	domain = None
	resource = None

	if "@" in user_str:
		# @user@domain format
		domain = user_str.split("@")[-1]
		resource = f"acct:{user_str}"
	elif user_str.startswith("https://"):
		# https://domain/user format
		domain = user_str.split("/")[2]
		resource = user_str
	else:
		# invalid format; return null
		return None

	if domain == "pleasedontpoke.me":
		return None

	# Use Webfinger to query the profile resource: https://tools.ietf.org/html/rfc7033#section-3.1
	request = get(f"https://{domain}/.well-known/webfinger?resource={resource}")
	if request.status_code != 200:
		return None

	info = request.json()

	# get "proper" user id
	user_id = info.get("subject")
	if not user_id:
		return None

	# get ActivityPub endpoint
	ap_url = None
	html_url = None
	for link in info.get("links") or []:
		if link.get("type") == "application/activity+json" or link.get("type") == "application/ld+json":
			ap_url = link.get("href")
		if link.get("type") == "text/html":
			html_url = link.get("href")

	if not ap_url:
		return None

	return {
		"id": user_id,
		"ap_url": ap_url,
		"html_url": html_url
	}

def ap_get_user(username):
	"""
	Fetch user info using Webfinger & add to our database

	username: someone@example.com

	Returns a User entity
	"""

	# Get profile links/metadata using Webfinger
	links = ap_get_links(username)

	# Check that user does not already exist
	user = dao.get_user(links.get("id"))
	if user:
		return user

	# Get ActivityPub JSON data for profile information: https://www.w3.org/TR/activitypub/#actor-objects
	profile_request = get(
		links.get("ap_url"),
		headers={"Accept": "application/activity+json"}
	)
	profile_json = profile_request.json()

	return dao.create_user(
		username,
		name=profile_json.get("name") or username,
		bio=profile_json.get("summary") or "",
		image=(profile_json.get("icon") or {}).get("url"),
		url=profile_json.get("url") or links.get("html_url"),
		ap_url=links.get("ap_url")
	)

def ap_poke_user(session_user, user, new_poke):
	"""
	Called after a poke has been created internally
	- sends user@example.com a Note (in a Create activity) to inform them of the poke
	"""

	activity_id = f"https://pleasedontpoke.me/users/{session_user['id']}/activity/{new_poke.id}"
	actor_id = f"https://pleasedontpoke.me/users/{session_user['id']}"
	note_id = f"https://pleasedontpoke.me/users/{session_user['id']}/poke/{new_poke.id}"

	published = new_poke["created"].replace(microsecond=0).isoformat() + "Z"

	# Creates a new note object with hardcoded message
	activity = {
		"@context": "https://www.w3.org/ns/activitystreams",
		"id": activity_id,
		"type": "Create",
		"actor": actor_id,
		"object": {
			"id": note_id,
			"type": "Note",
			"attributedTo": actor_id,
			"content": "Get poked.",
			"published": published
		},
		"published": published,
		"to": [f"acct:{user['id']}"],
		"cc": ["https://www.w3.org/ns/activitystreams#Public"]
	}

	# send to remote site as a POST request
	url = user["ap_url"]
	post(url, activity.json())
