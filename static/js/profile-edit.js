const editImage = document.getElementById("profile-image-edit");
const editImageInput = document.getElementById("profile-image-input");
const editImageForm = document.getElementById("profile-image-form");

editImage && editImage.addEventListener("click", () => {
	// open the image input when clicked
	editImageInput.click();
});

editImageInput && editImageInput.addEventListener("input", () => {
	// when image entered, submit the form
	editImageForm.submit();
});
