from google.cloud import datastore
from datetime import datetime, timedelta

# pleasedontpoke.me/@user1@othersite.com
# othersite.com/@user1
# user1@acufuncture.com

# @user1@othersite.com "poke @user1@pleasedontpoke.me"

# users: []
#   create_user
#   query_users(id)
#   get_user()
# pokes: []
#   create_poke
#   query_sender_pokes(userId)
#   query_receiver_pokes(userId)

USER_ENTITY_TYPE = "user"
POKE_ENTITY_TYPE = "poke"

class Datastore:
	def __init__(self):
		self.client = datastore.Client()

	def create_user(self, username, password, salt):
		"""Create, store, and return a user entity."""
		user_key = self.client.key(USER_ENTITY_TYPE, username)
		user = datastore.Entity(key=user_key)
		user["id"] = username
		user["name"] = username
		user["bio"] = ""
		user["image"] = "/static/img/profile.png"
		user["friends"] = []
		user["pokes"] = 0
		user["created"] = datetime.now()
		user["password"] = password
		user["salt"] = salt
		self.client.put(user)
		return user

	def get_user(self, id):
		"""Retrieve a user with their corresponding username."""
		user_key = self.client.key(USER_ENTITY_TYPE, id)
		user = self.client.get(user_key)
		return user

	def update_user(self, user_edit):
		"""Update the properties of a user with the edited values."""
		user_key = self.client.key(USER_ENTITY_TYPE, user_edit['id'])
		user = self.client.get(user_key)
		# Only update properties if they exist in user_edit
		if "name" in user_edit:
			user["name"] = user_edit["name"]
		if "bio" in user_edit:
			user["bio"] = user_edit["bio"]
		if "image" in user_edit:
			user["image"] = user_edit["image"]
		if "pokes" in user_edit:
			user["pokes"] = user_edit["pokes"]
		if "friends" in user_edit:
			user["friends"] = user_edit["friends"]

		self.client.put(user)
		return user

	def query_users(self, name, search_limit=6):
		"""Perform a substring query of name to usernames and return the results as a list."""
		# Rough username search by prefix
		query = self.client.query(kind=USER_ENTITY_TYPE)
		# Filter by "> name" and "< name + z" (index value must be within that of the provided string)
		name_z = name + "z"
		query.add_filter("id", ">=", name)
		query.add_filter("id", "<=", name_z)
		# Limit number of results to hardcoded value
		results = query.fetch(limit=search_limit)
		return list(results)

	def create_poke(self, poker, pokee):
		"""Create a poke entity and store it in Datastore. Increment, update, and return pokee's poke total."""
		poker_key = self.client.key(USER_ENTITY_TYPE, poker)
		poke_key = self.client.key(POKE_ENTITY_TYPE, parent=poker_key)
		poke = datastore.Entity(key=poke_key)
		poke["created"] = datetime.now()
		poke["poker"] = poker
		poke["pokee"] = pokee

		pokee_entity = self.get_user(pokee)
		pokee_entity["pokes"] += 1

		self.client.put(pokee_entity)
		self.client.put(poke)

	def query_pokes_sent_between(self, poker, pokee, after_date=None, result_limit=10000):
		"""Return a list of pokes sent from one user to another specific user."""
		poker_key = self.client.key(USER_ENTITY_TYPE, poker)
		query = self.client.query(kind=POKE_ENTITY_TYPE, ancestor=poker_key)
		query.add_filter("pokee", "=", pokee)

		if after_date is not None:
			query.add_filter("created", ">", after_date)

		# sort created index in descending order (newest first)
		query.order = ["-created"]

		results = query.fetch(limit=result_limit)
		return list(results)

	def query_pokes_sent_by(self, poker, after_date=None, result_limit=10000):
		"""Return a list of pokes a user has sent."""
		poker_key = self.client.key(USER_ENTITY_TYPE, poker)
		query = self.client.query(kind=POKE_ENTITY_TYPE, ancestor=poker_key)

		if after_date is not None:
			query.add_filter("created", ">", after_date)

		# sort created index in descending order (newest first)
		query.order = ["-created"]

		results = query.fetch(limit=result_limit)
		return list(results)

	def query_pokes_sent_to(self, pokee, before_date=None, after_date=None, result_limit=10000):
		"""Return a list of pokes a user has received."""
		query = self.client.query(kind=POKE_ENTITY_TYPE)
		query.add_filter("pokee", "=", pokee)

		# if before_date is unset, find pokes before "now"
		if before_date is None:
			before_date = datetime.now()

		# filter by created date params (must occur before {before_date} and after {after_date})
		query.add_filter("created", "<=", before_date)
		if after_date is not None:
			query.add_filter("created", ">", after_date)

		# sort created index in descending order (newest first)
		query.order = ["-created"]

		results = query.fetch(limit=result_limit)
		return list(results)

dao = Datastore()
