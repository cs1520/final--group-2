from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def home():
    """Return the user's home page."""
    print("Hit the route!")
    return render_template("index.html")

@app.route("/login")
def login():
	"""Return the login / sign-up page."""
	return render_template("login.html")

@app.route("/@<user>")
def user(user):
    """Return the user profile page."""
    return render_template("user.html",
		user={"username": user, "displayName": "Moby Dick", "profileImage": "https://media.pri.org/s3fs-public/styles/story_main/public/images/2019/08/2031_episodeimage.jpg"})

@app.route("/search")
def search():
	"""Return the results for a search query."""
	return render_template("search.html",
		query = request.args.get('q'))

@app.route("/friends")
def friends():
	"""Return the user's friends list."""
	return render_template("friends.html")

@app.route("/notifications")
def notifications():
	"""Return the user's recent pokes."""
	return render_template("notifications.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True) 
