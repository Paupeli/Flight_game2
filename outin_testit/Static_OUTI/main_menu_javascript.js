'use strict';

document.getElementById("old-user-btn").addEventListener("click", () => {
  window.location.href = "/old_user";
});
document.getElementById("new-user-btn").addEventListener("click", () => {
  window.location.href = "/new_user";
});

document.getElementById("quit-btn").addEventListener("click", () => {
  window.location.href = "/start";                                                                                /// TOISTOA POISTA LOPUKSI
});

