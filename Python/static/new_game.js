'use strict'

document.getElementById("old-user-btn").addEventListener("click", () => {
  window.location.href = "/old_user"; //vanha käyttäjä
});
document.getElementById("new-user-btn").addEventListener("click", () => {
  window.location.href = "/new_user"; //uusi käyttäjä
});

document.getElementById("quit-btn").addEventListener("click", () => {
  window.location.href = "/start"; //byeee
});
