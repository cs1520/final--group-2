document.addEventListener("load", () => {
	const searchForm = document.getElementById("search-form");
	const searchInput = document.getElementById("search-input");

	// submit the search query on enter
	searchInput && searchInput.addEventListener("keyup", (event) => {
		if (event.key !== "Enter") return;

		searchForm.submit();
	});
});
