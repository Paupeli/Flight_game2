'use strict';

//näistä ku klikkailee ni pääsee noille sivuille mihin ne on linkitetty

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("btn-continue").addEventListener("click", () => sendOption("continue"));
    document.getElementById("btn-scoreboard").addEventListener("click", () => sendOption("check scoreboard"));
    document.getElementById("btn-rules").addEventListener("click", () => sendOption("rules"));
    document.getElementById("btn-main-menu").addEventListener("click", () => sendOption("main menu"));
    document.getElementById("btn-quit").addEventListener("click", () => sendOption("quit"));
});


async function sendOption(option) { //hakee dataa ja parsii sen
    try {
        const response = await fetch('/pause', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ option })
        });

        const data = await response.json();
        const output = document.getElementById('pause-response');

        if (response.ok) {
            if (data.status === 'redirect' && data.location) {
                window.location.href = data.location;
                return;
            }

            output.innerHTML = `
                <strong>Status:</strong> ${data.status || 'paused'}<br>
                ${data.message || data.data || ''}
            `;
        } else {
            output.innerHTML = `<strong>Error:</strong> ${data.error}`;
        }
    } catch (err) {
        document.getElementById('pause-response').innerHTML = 'Error connecting to server.';
        console.error(err); //error handling
    }
}
