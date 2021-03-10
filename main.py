from flask import Flask, redirect, url_for, render_template, request


app = Flask(__name__)

testusers = [
	{
	"id": "mobydick",
	"name": "Moby Dick",
	"image": "https://media.pri.org/s3fs-public/styles/story_main/public/images/2019/08/2031_episodeimage.jpg",
	"bio": "Ishmael describes Moby Dick as having two prominent white areas around \"a peculiar snow-white wrinkled forehead, and a high, pyramidical white hump\", the rest of his body being of stripes and patches between white and gray.",
	"pokes": 50,
	"pokers": 9
	},
	{"id": "ahab",
	"name": "Captain Ahab",
	"image": "https://betterlivingthroughbeowulf.com/wp-content/uploads/2011/11/Captain-Ahab.jpg",
	"bio": "I want to catch that white whale!",
	"pokes": 99,
	"pokers": 35
	},
	{
	"id": "batman",
	"name": "NotWayne Batman",
	"image": "https://m.media-amazon.com/images/M/MV5BOTM3MTRkZjQtYjBkMy00YWE1LTkxOTQtNDQyNGY0YjYzNzAzXkEyXkFqcGdeQXVyOTgwMzk1MTA@._V1_UY1200_CR85,0,630,1200_AL_.jpg",
	"bio": "I'm Batman.",
	"pokes": 250,
	"pokers": 58
	},
	{
	"id": "tonystark",
	"name": "Tony Stark",
	"image": "https://i.pinimg.com/originals/cd/71/1f/cd711fca60134229d08e3f8e6604674b.jpg",
	"bio": "Ay, it's me Tony!",
	"pokes": 100,
	"pokers": 12
	},
	{
	"id": "harrypotter",
	"name": "Harry Potter",
	"image": "https://images-na.ssl-images-amazon.com/images/I/91b8oNwaV1L.jpg",
	"bio": "In a certain kingdom, in a certain land, there lived a widowed merchant. He had a son, a daughter, and a brother. One day the merchant was getting ready to sail to foreign lands to sell various goods. He planned to take his son with him and leave his daughter at home. Before leaving, he summoned his brother and said to him: I leave my entire household in your hands, dear brother, and I beg you to look after my daughter.",
	"pokes": 42,
	"pokers": 4
	},
	{
	"id": "doomguy",
	"name": "The Doom Slayer",
	"image": "https://giantbomb1.cbsistatic.com/uploads/scale_small/8/87790/3068872-doom.png",
	"bio": "In the first age, in the first battle, when the shadows first lengthened, one stood. He chose the path of perpetual torment. In his ravenous hatred he found no peace. And with boiling blood he scoured the Umbral Plains seeking vengeance against the dark lords who had wronged him. And those that tasted the bite of his sword named him... The Doom Slayer.",
	"pokes": 1,
	"pokers": 9
	}
]

testuser = {
	"id": "mobydick",
	"name": "Moby Dick",
	"image": "https://media.pri.org/s3fs-public/styles/story_main/public/images/2019/08/2031_episodeimage.jpg",
	"bio": "Ishmael describes Moby Dick as having two prominent white areas around \"a peculiar snow-white wrinkled forehead, and a high, pyramidical white hump\", the rest of his body being of stripes and patches between white and gray.",
	"pokes": 50,
	"pokers": 9
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

@app.route("/@<user>", methods=["POST", "GET"])
def user(user):
	endpointUser = getuser(user)
	"""Return, and potentially poke, the user profile page."""
	if request.method == "POST":
		endpointUser["pokes"] += 1
	return render_template("user.html",
		page = { "user": endpointUser },
		user = testuser)

@app.route("/search")
def search():
	"""Return the results for a search query."""
	user = request.args.get('')
	return render_template("search.html",
		page = { "query": request.args.get('q') },
		user = getuser(request.args.get('q')))

@app.route("/friends")
def friends():
	"""Return the user's friends list."""
	return render_template("friends.html",
		page = {"friends": testusers},
		user = testuser)

@app.route("/notifications")
def notifications():
	"""Return the user's recent pokes."""
	return render_template("notifications.html",
		page = { "pokes": testusers },
		user = testuser)

def getuser(user):
	"""Return the user with the specified id."""
	for tu in testusers:
		if tu["id"] == user:
			return tu
	return None

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
