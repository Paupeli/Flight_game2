'use strict'

fetch("/new_game/old_user/fetch")
    .then(response => response.json())
    .then(data => {
        const insideTable = document.getElementById('insideTable');
        data.forEach(username => {
            const button = document.createElement('button');

            button.textContent = username;
            button.className = 'username-button';

            button.addEventListener('click', () => {
                sessionStorage.setItem('username', username);              //Lisätty vanhan käyttäjän tallennus !!
                window.location.href = '/new_game/pick_length';
            });
            insideTable.appendChild(button);
        });
    });
document.getElementById("new_game-btn").addEventListener("click", () => {
  window.location.href = "/new_game";
});
document.getElementById("main_menu-btn").addEventListener("click", () => {
  window.location.href = "/main_menu";
});
document.getElementById("quit-btn").addEventListener("click", () => {
  window.location.href = "/start";
});