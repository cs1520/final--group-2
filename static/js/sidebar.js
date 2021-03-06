window.addEventListener("load", () => {
	const sidebar = document.getElementById("sidebar");
	const sidebarToggle = document.getElementById("sidebar-toggle");

	sidebarToggle && sidebarToggle.addEventListener("click", (e) => {
		e.preventDefault();

		// toggle sidebar "hidden" attribute
		if (sidebar.getAttribute("hidden")) {
			sidebar.removeAttribute("hidden");
		} else {
			sidebar.setAttribute("hidden", "true");
		}

		return false;
	});
});
