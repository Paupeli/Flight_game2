'use strict'

document.getElementById("old-user-btn").addEventListener("click", () => {
  window.location.href = "/new_game/old_user"; //vanha käyttäjä
});
document.getElementById("new-user-btn").addEventListener("click", () => {
  window.location.href = "/new_game/new_user"; //uusi käyttäjä
});

document.getElementById("quit-btn").addEventListener("click", () => {
  window.location.href = "/start"; //byeee
});

document.getElementById("main_menu-btn").addEventListener("click", () => {
  window.location.href = "/main_menu"; //main menuun menee tämä
});