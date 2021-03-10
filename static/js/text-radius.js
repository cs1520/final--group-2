// query any element with the "data-text-radius" attribute
document.querySelectorAll(".text-radius").forEach((element) => {
	// replace innerHTML with individual spans per char
	element.innerHTML = element.innerText.split('').map((char, index) => {
		return `<span style="--text-radius-deg: ${index * 7}deg;">${char}</span>`;
	}).join('');
});
