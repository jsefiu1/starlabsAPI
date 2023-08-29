document.addEventListener("DOMContentLoaded", function () {
  const body = document.querySelector("body");
  body.style.opacity = 0;

  const fadeIn = () => {
      let opacity = parseFloat(body.style.opacity);
      if (opacity < 1) {
          opacity += 0.02;
          body.style.opacity = opacity;
          requestAnimationFrame(fadeIn);
      }
  };

  fadeIn();
});