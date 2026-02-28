/**
 * Cannabisers — minimal JS
 * Scroll behavior, smooth anchor links, FAQ accordion
 */

(function () {
  "use strict";

  // Header scroll effect
  var header = document.querySelector(".header");
  if (header) {
    var lastScroll = 0;
    window.addEventListener(
      "scroll",
      function () {
        var scrollY = window.scrollY || window.pageYOffset;
        if (scrollY > 60) {
          header.classList.add("header--scrolled");
        } else {
          header.classList.remove("header--scrolled");
        }
        lastScroll = scrollY;
      },
      { passive: true }
    );
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var target = document.querySelector(a.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  // Close desktop dropdowns on outside click
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".nav__item--dropdown")) {
      document
        .querySelectorAll(
          ".nav--desktop .nav__item--dropdown.active"
        )
        .forEach(function (d) {
          d.classList.remove("active");
          d.querySelector(".nav__dropdown-toggle").setAttribute(
            "aria-expanded",
            "false"
          );
        });
    }
  });

  // Desktop dropdown hover
  document
    .querySelectorAll(".nav--desktop .nav__item--dropdown")
    .forEach(function (item) {
      item.addEventListener("mouseenter", function () {
        item.classList.add("active");
        item.querySelector(".nav__dropdown-toggle").setAttribute(
          "aria-expanded",
          "true"
        );
      });
      item.addEventListener("mouseleave", function () {
        item.classList.remove("active");
        item.querySelector(".nav__dropdown-toggle").setAttribute(
          "aria-expanded",
          "false"
        );
      });
    });
})();
