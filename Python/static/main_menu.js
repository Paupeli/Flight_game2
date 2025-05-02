'use strict';

document.getElementById("new_game-btn").addEventListener("click", () => {
  window.location.href = "/new_game"; //tähän linkittyy hahmon luonti/valinta sivu
});
document.getElementById("rules-btn").addEventListener("click", () => {
  window.location.href = "/rules"; //tähän linkittyy rules/instructions sivu
});

document.getElementById("scoreboard-btn").addEventListener("click", () => {
  window.location.href = "/scoreboard"; //tähän linkittyy scoreboard sivu
});

document.getElementById("quit-btn").addEventListener("click", () => {
  window.location.href = "/start"; //tästä klikkaamalla palataan aloitussivulle
});