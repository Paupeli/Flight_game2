'use strict'

document.getElementById('create-user-btn').addEventListener('click', () => {
    const username = document.getElementById('username-input').value.trim();
    
    if (!username) {
        alert('Please enter a username');
        return;
    }
localStorage.setItem('username', username);

     fetch(`/new_game/new_user/${username}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.username) {
            sessionStorage.setItem('username', username);
            window.location.href = '/new_game/pick_length';
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
