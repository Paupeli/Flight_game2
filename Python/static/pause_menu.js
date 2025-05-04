'use strict';

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("btn-continue").addEventListener("click", () => sendOption("continue"));
    document.getElementById("btn-scoreboard").addEventListener("click", () => sendOption("check scoreboard"));
    document.getElementById("btn-rules").addEventListener("click", () => sendOption("rules"));
    document.getElementById("btn-quit").addEventListener("click", () => sendOption("quit"));
});

async function sendOption(option) {
    try {
        const response = await fetch('/pause', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ option })
        });

        const data = await response.json();
        const output = document.getElementById('pause-response');

        if (response.ok) {
            output.innerHTML = `
                <strong>Status:</strong> ${data.status || 'paused'}<br>
                ${data.message || data.data || ''}
            `;
        } else {
            output.innerHTML = `<strong>Error:</strong> ${data.error}`;
        }

        if (data.status === 'quitting') {
            setTimeout(() => {
                window.location.href = '/start';
            }, 2000);
        }
    } catch (err) {
        document.getElementById('pause-response').innerHTML = 'Error connecting to server.';
        console.error(err);
    }
}