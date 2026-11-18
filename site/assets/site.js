document.querySelectorAll("table").forEach((table) => {
  const wrapper = document.createElement("div");
  wrapper.className = "table-scroll";
  wrapper.tabIndex = 0;
  wrapper.setAttribute("role", "region");
  wrapper.setAttribute("aria-label", "Scrollable data table");
  table.before(wrapper);
  wrapper.append(table);
});

document.querySelectorAll("[data-youtube-id]").forEach((button) => {
  button.addEventListener("click", () => {
    const frame = document.createElement("iframe");
    frame.src = "https://www.youtube-nocookie.com/embed/" + button.dataset.youtubeId + "?autoplay=1";
    frame.title = "Sixfold film";
    frame.allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture";
    frame.allowFullscreen = true;
    button.parentElement.replaceChildren(frame);
    frame.focus();
  });
});

document.querySelectorAll("nav a").forEach((link) => {
  if (link.href === window.location.href.split("#")[0]) {
    link.setAttribute("aria-current", "page");
  }
});

const films = document.querySelectorAll("video");
films.forEach((film) => {
  film.addEventListener("play", () => {
    films.forEach((other) => {
      if (other !== film) other.pause();
    });
  });
});
