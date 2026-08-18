(function () {
  "use strict";

  var videos = document.querySelectorAll("video[data-lazy-video]");
  var prefersReducedMotion = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function loadVideo(video) {
    var sources = video.querySelectorAll("source[data-src]");

    sources.forEach(function (source) {
      source.src = source.dataset.src;
      source.removeAttribute("data-src");
    });

    video.load();
    if (!prefersReducedMotion) {
      var playPromise = video.play();
      if (playPromise) {
        playPromise.catch(function () {});
      }
    }
  }

  if (!("IntersectionObserver" in window)) {
    videos.forEach(loadVideo);
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        loadVideo(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { rootMargin: "300px 0px" });

  videos.forEach(function (video) {
    observer.observe(video);
  });
}());
