from flask import Flask, render_template, request


app = Flask(__name__)

testuser = {
	"id": "mobydick",
	"name": "Moby Dick",
	"image": "https://media.pri.org/s3fs-public/styles/story_main/public/images/2019/08/2031_episodeimage.jpg",
	"bio": "Ishmael describes Moby Dick as having two prominent white areas around \"a peculiar snow-white wrinkled forehead, and a high, pyramidical white hump\", the rest of his body being of stripes and patches between white and gray."
}

@app.route("/")
def home():
    """Return the user's home page."""
    print("Hit the route!")
    return render_template("index.html",
		page = {},
		user = testuser)

@app.route("/login")
@app.route("/register")
def login():
	"""Return the login / sign-up page."""
	return render_template("login.html")

@app.route("/@<user>")
def user(user):
    """Return the user profile page."""
    return render_template("user.html",
		page = { "user": { "id": user, "name": testuser["name"], "image": testuser["image"] }},
		user = testuser)

@app.route("/search")
def search():
	"""Return the results for a search query."""
	return render_template("search.html",
		page = { "query": request.args.get('q') },
		user = testuser)

@app.route("/friends")
def friends():
	"""Return the user's friends list."""
	return render_template("friends.html",
		page = {},
		user = testuser)

@app.route("/notifications")
def notifications():
	"""Return the user's recent pokes."""
	return render_template("notifications.html",
		page = {},
		user = testuser)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
