function showDescription(text) {
  document.getElementById("description").innerText = text;
  document.getElementById("modal").style.display = "flex";
}

function closeModal() {
  document.getElementById("modal").style.display = "none";
}
