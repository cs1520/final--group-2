from flask import render_template, request, session, jsonify
from requests import get, post

from main import app, render_page
from datastore import dao

from datetime import datetime, timedelta
from werkzeug.http import http_date
from httpsig import HeaderSigner

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

	if user_str.startswith("https://"):
		# https://domain/user format
		domain = user_str.split("/")[2]
		resource = user_str
	elif "@" in user_str:
		# @user@domain format
		domain = user_str.split("@")[-1]
		resource = f"acct:{user_str}"
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

	# get the "proper" user id (and ensure that it matches the requested domain)
	user_id = info.get("subject")
	if (not user_id) or (not user_id.endswith("@" + domain)):
		return None

	# get the user's ActivityPub actor urls
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
		"id": user_id.split("acct:")[-1],
		"ap_url": ap_url,
		"html_url": html_url
	}

def ap_fetch_user(user_str):
	"""
	Fetch user info using Webfinger & add to our database

	username: someone@example.com

	Returns a User entity
	"""

	# Get profile links/metadata using Webfinger
	links = ap_get_links(user_str)
	if not links:
		return None

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
	profile_inbox = profile_json.get("inbox") or links.get("ap_url")
	profile_pubkey = (profile_json.get("publicKey") or {}).get("publicKeyPem") # get public key from remote profiles

	return dao.create_user(
		links.get("id"),
		name=profile_json.get("name") or links.get("id"),
		bio=profile_json.get("summary") or "",
		image=(profile_json.get("icon") or {}).get("url"),
		url=profile_json.get("url") or links.get("html_url"),
		ap_url=links.get("ap_url"),
		ap_inbox_url=profile_inbox,
		rsa_pubkey=profile_pubkey
	)

def ap_poke_user(session_user, user, new_poke):
	"""
	Called after a poke has been created internally
	- sends user@example.com a Note (in a Create activity) to inform them of the poke
	"""

	timestamp = int(new_poke["created"].timestamp())

	activity_id = f"https://pleasedontpoke.me/users/{session_user['id']}/poke/{timestamp}/activity"
	actor_id = f"https://pleasedontpoke.me/users/{session_user['id']}"
	note_id = f"https://pleasedontpoke.me/users/{session_user['id']}/poke/{timestamp}"

	published = new_poke["created"].replace(microsecond=0).isoformat() + "Z"

	# Creates a new note object with hardcoded message
	activity = {
		"@context": "https://www.w3.org/ns/activitystreams",
		"id": activity_id,
		"type": "Create",
		"actor": actor_id,
		"object": {
			"@context": "https://www.w3.org/ns/activitystreams",
			"id": note_id,
			"type": "Note",
			"attributedTo": actor_id,
			"published": published,
			"url": note_id,
			"atomUri": note_id,
			"content": f'👉 <span class="h-card"><a href="{user["ap_url"]}" class="u-url mention">@<span>{user["id"]}</span></a></span> poke.',
			"to": ["https://www.w3.org/ns/activitystreams#Public"],
			"cc": [user["ap_url"]],
			"tag": [{
				"type": "Mention",
				"href": user["ap_url"],
				"name": "@" + user["id"]
			}]
		},
		"published": published,
		"to": ["https://www.w3.org/ns/activitystreams#Public"],
		"cc": [user["ap_url"]]
	}

	# send to remote site as a POST request
	url = user["ap_inbox_url"]
	post(
		url,
		json=activity,
		headers=ap_get_signed_headers(url, session_user)
	)

def ap_get_signed_headers(url, user):
	# Sign outgoing requests with the user's RSA key
	hs = HeaderSigner(
		f"https://pleasedontpoke.me/users/{user['id']}#main-key",
		user["rsa_privkey"],
		algorithm="rsa-sha256",
		headers=["(request-target)", "host", "date", "content-type"],
		sign_header="Signature"
	)

	# Construct signed header dict
	return hs.sign(
		{
			"Date": http_date(),
			"Content-Type": "application/activity+json"
		},
		method="POST",
		host=url.split("/", 3)[-2],
		path="/" + url.split("/", 3)[-1]
	)
