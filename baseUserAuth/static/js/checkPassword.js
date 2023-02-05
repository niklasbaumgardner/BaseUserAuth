"use strict";

function checkPasswordsEqual() {
  let password1 = document.getElementById("password1").value;
  let password2 = document.getElementById("password2");
  let invalidMessage = password2.nextElementSibling;
  password2 = password2.value;

  if (password2.length < password1.length) {
    invalidMessage.classList.remove("display-block");
  } else {
    if (password1 === password2) {
      invalidMessage.classList.remove("display-block");
    } else {
      invalidMessage.classList.add("display-block");
    }
  }
}

let password1 = document.getElementById("password1");
let password2 = document.getElementById("password2");

password1.addEventListener("input", checkPasswordsEqual);
password2.addEventListener("input", checkPasswordsEqual);
