'use strict'

document.getElementById('create-user-btn').addEventListener('click', () => {
    const username = document.getElementById('username-input').value.trim();
    
    if (!username) {
        alert('Please enter a username');
        return;
    }

    fetch('/new_game/new_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ new_screen_name: username })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            window.location.href = `/new_game/old_user/${username}`;
        } else {
            alert(result.error || 'Failed to create new username');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Something went wrong');
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
