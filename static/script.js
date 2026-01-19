const btn = document.getElementById("backToTop");

window.onscroll = () => {
  btn.style.display = window.scrollY > 200 ? "block" : "none";
};

btn.onclick = () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
};

