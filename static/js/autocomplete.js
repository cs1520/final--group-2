const names = ["Jacob", "James", "Jason", "Bader", "Moby Dick", "John Doe", "CS1520"]

window.addEventListener("load", () => {
	const searchForm = document.getElementById("search-form");
	const searchInput = document.getElementById("search-input");
	const searchList = document.getElementById("search-list");
	//TODO: Implement previous searches in suggestions

	function updateNames() {
		let namesArray = [];

		if (searchInput.value) {
			namesArray = names.filter(name => name.toLowerCase().includes(searchInput.value.toLowerCase()));
			namesArray = namesArray.map(name => `<li><a class="button" href="/@mobydick">${name}</a></li>`);
		}

		searchList.innerHTML = namesArray.join("") || '<small>No results found.</small>';
	}

	searchInput.addEventListener("input", updateNames);
	updateNames();
});
