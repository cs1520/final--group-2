import { debounce, allStorage } from './utils.js';

const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const searchList = document.getElementById("search-list");
const searchButton = document.getElementById("searchButton");

//TODO: Store recent searches in users
//Show at most 2 recent searches?
//Have an icon (clock symbol) for recent search
//Should it persist in user's data, or just during their session?
//Putting the previous searches into local storage

//Use search_json() to generate a JSON array

async function updateNames() {
	// remove any leading '@' symbol from the username
	const name = searchInput.value.replace(/^\@/, '').toLowerCase();

	let results = [];
	if (name) {
		// invoke the search endpoint with url-encoded query
		results = await fetch("/api/search?q=" + encodeURIComponent(name))
			.then(response => response.json());
	} else {
		// get previous searches from localStorage
		results = Object.values(allStorage("autocomplete-"))
			.map((str) => JSON.parse(str));

		// sort by date (descending order)
		results.sort((a, b) => b.date - a.date);

		// obtain first 6 elements from results
		results = results.splice(0, 6);
	}

	// format results as HTML array
	const namesArray = results.map(user => {
		// convert user to a json object (with escaped quote chars)
		let userJson = JSON.stringify(user).replace(/\"/g, "&quot;");
		return `<li><a class="button searchButton" data-user="${userJson}" href="/@${user.id}">
			${name ? '' : '<i class="material-icons">history</i>'}
			<span>${user.name}</span>
		</a></li>`
	});
	searchList.innerHTML = namesArray.join("") || '<small>No results found.</small>';

	document.querySelectorAll(".searchButton").forEach((element) => {
		const user = element.getAttribute("data-user");
		element.onclick = function() {
			insertRecentSearch(JSON.parse(user));
		};
	});
}

function insertRecentSearch(user) {
	user.date = Date.now();
	// insert user object into local storage as "id": "{ id, name, date }"
	localStorage.setItem("autocomplete-" + user.id, JSON.stringify(user));
}

//Adds 250ms delay for each key press (to prevent spamming the search endpoint)
const callback = debounce(updateNames, 250);

searchInput.addEventListener("input", () => {
	callback();
});


updateNames();
