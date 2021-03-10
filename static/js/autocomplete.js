const names = ["Jacob", "James", "Jason", "Bader", "Moby Dick", "John Doe", "CS1520"]

window.addEventListener("load", () => {
	const searchForm = document.getElementById("search-form");
	const searchInput = document.getElementById("search-input");
	//TODO: Implement previous searches in suggestions

	//This only works for all lower case input
	searchInput.addEventListener("input", (e)=> {
		let namesArray = [];

		if(e.target.value) {
			namesArray = names.filter(name => name.toLowerCase().includes(e.target.value));
			//Quick fix to unbullet list
			namesArray = namesArray.map(name => `<li style="list-style: none">${name}</li>`);
		}
		showNames(namesArray);
	})
});
function showNames(namesArray){

	const html = !namesArray.length ? '' : namesArray.join("");
	document.querySelector("ul").innerHTML = html;
}
