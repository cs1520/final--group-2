const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebar-toggle");

sidebarToggle && sidebarToggle.addEventListener("click", (e) => {
	e.preventDefault();

	// toggle sidebar attribute (referenced in CSS)
	if (sidebar.getAttribute("toggled")) {
		sidebar.removeAttribute("toggled");
	} else {
		sidebar.setAttribute("toggled", "true");
	}

	return false;
});
