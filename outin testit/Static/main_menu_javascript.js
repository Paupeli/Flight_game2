'use strict';

document.getElementById("saved-user-btn").addEventListener("click", () => {
  window.location.href = "/saved_user";
});
document.getElementById("new-user-btn").addEventListener("click", () => {
  window.location.href = "/new_user";
});

document.getElementById("quit-btn").addEventListener("click", () => {
  window.location.href = "/start";                                                                                /// TOISTOA POISTA LOPUKSI
});

