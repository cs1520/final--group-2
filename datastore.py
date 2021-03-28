from google.cloud import datastore
from datetime import datetime

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
SEARCH_RESULT_LIMIT = 6

class Datastore:
	def __init__(self):
		self.client = datastore.Client()

	def create_user(self, username, password, salt):
		"""Create, store, and return a user entity."""
		user_key = self.client.key(USER_ENTITY_TYPE, username)
		user = datastore.Entity(key=user_key)
		user["id"] = username
		user["name"] = username
		user["bio"] = "This user hasn't changed their bio yet. You should poke them."
		user["image"] = "/static/img/profile.png"
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

	def query_users(self, name):
		"""Perform a substring query of name to usernames and return the results as a list."""
		# Rough username search by prefix
		query = self.client.query(kind=USER_ENTITY_TYPE)
		# Filter by "> name" and "< name + z" (index value must be within that of the provided string)
		name_z = name + "z"
		query.add_filter("id", ">=", name)
		query.add_filter("id", "<=", name_z)
		# Limit number of results to hardcoded value
		results = query.fetch(limit=SEARCH_RESULT_LIMIT)
		return list(results)

	def create_poke(self, poker, pokee):
		"""Create a poke entity and store it in Datastore. Increment and update pokee's poke total."""
		poke_key = self.client.key(POKE_ENTITY_TYPE)
		poker_key = self.client.key(USER_ENTITY_TYPE, poker)
		poke = datastore.Entity(key=poke_key, parent=poker_key)
		poke["created"] = datetime.now()
		poke["pokee"] = pokee
		

		pokee_entity = get_user(pokee)
		pokee_entity["pokes"] += 1

		self.client.put(pokee_entity)
		self.client.put(poke)

	def query_pokes_sent_between(self, poker, pokee):
		"""Return a list of pokes sent from one user to another specific user."""
		poker_key = self.client.key(USER_ENTITY_TYPE, poker)
		query = self.client.query(kind=POKE_ENTITY_TYPE, ancestor=poker_key)
		query.add_filter("pokee", "=", pokee)
		results = query.fetch()
		return list(results)

	def query_pokes_sent_by(self, poker):
		"""Return a list of pokes a user has sent."""
		poker_key = self.client.key(USER_ENTITY_TYPE, poker)
		query = self.client.query(kind=POKE_ENTITY_TYPE, ancestor=poker_key)
		results = query.fetch()
		return list(results)
	
	def query_pokes_sent_to(self, pokee):
		"""Return a list of pokes a user has received."""
		query = self.client.query(kind=POKE_ENTITY_TYPE)
		query.add_filter("pokee", "=", pokee)
		results = query.fetch()
		return list(results)


dao = Datastore()
