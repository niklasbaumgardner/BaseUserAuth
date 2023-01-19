"use strict";

async function sendUsernameRequest(username) {
  let response = await fetch(USERNAME_UNIQUE_URL + "?" + new URLSearchParams({
    username,
  }));
  response = await response.json();
  return response;
}

async function sendEmailRequest(email) {
  let response = await fetch(EMAIL_UNIQUE_URL + "?" + new URLSearchParams({
    email,
  }));
  response = await response.json();
  return response;
}

let usernameInput = document.getElementById("username");
usernameInput.addEventListener("input", async event => {
  let orginalValue = event.target.getAttribute("original-value");
  let newValue = event.target.value;
  let invalidMessage = event.target.nextElementSibling;

  if (orginalValue === newValue) {
    // don't need to send request
    invalidMessage.classList.remove("display-block");
  } else {
    let result = await sendUsernameRequest(newValue);
    console.log("username is unique", result.isUnique);

    if (result.isUnique) {
      invalidMessage.classList.remove("display-block");
    } else {
      invalidMessage.classList.add("display-block");
    }
  }
});

let emailInput = document.getElementById("email");
emailInput.addEventListener("input", async event => {
  let orginalValue = event.target.getAttribute("original-value");
  let newValue = event.target.value;
  let invalidMessage = event.target.nextElementSibling;

  if (orginalValue === newValue) {
    // don't need to send request
    invalidMessage.classList.remove("display-block");
  } else {
    let result = await sendEmailRequest(event.target.value);
    console.log("email is unique", result.isUnique);

    if (result.isUnique) {
      invalidMessage.classList.remove("display-block");
    } else {
      invalidMessage.classList.add("display-block");
    }
  }
});