"use strict";

const storage = window["localStorage"];

function getTheme() {
  return storage.getItem("theme");
}

function getThemeButton(theme) {
  return document.querySelector(`[data-bs-theme-value="${theme}"]`);
}

function getThemeButtons() {
  return document.querySelectorAll("[data-bs-theme-value]");
}

function setTheme(theme) {
  theme = theme === "dark" ? "dark" : "light";

  // Set html element theme
  document.documentElement.setAttribute("data-bs-theme", theme);

  // Set all buttons to inactive
  for (let button of getThemeButtons()) {
    button.classList.remove("active");
  }

  // Set theme button to active
  let currentThemeButton = getThemeButton(theme);
  currentThemeButton.classList.add("active");

  currentThemeButton.parentElement.parentElement.previousElementSibling.innerText = currentThemeButton.innerText.trim();

  storage.setItem("theme", theme);
}


window.addEventListener("DOMContentLoaded", () => {
  let storedTheme = getTheme();
  setTheme(storedTheme);

  let themeButtons = getThemeButtons();

  for (let button of themeButtons) {
    button.addEventListener("click", () => {
      let theme = button.getAttribute("data-bs-theme-value");
      setTheme(theme);
    });
  }
});