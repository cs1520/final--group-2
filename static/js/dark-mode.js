
const darkButton = document.getElementById("dark-button");

/*Sets the page theme to localStorage*/

function dark_toggle() {
	let el1 = document.getElementById("dark-reader");

	if(el1.disabled) {
		el1.disabled = false;
		localStorage.setItem("darkreader", "enabled");
	} else {
		el1.disabled = true;
		localStorage.setItem("darkreader", "disabled");
	}
} 

darkButton.addEventListener("click", dark_toggle);

