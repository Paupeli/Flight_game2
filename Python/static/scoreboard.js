'use strict'

    fetch("/flight_game/scoreboard")
    .then(response => response.json())
    .then(data => {
        const insideTable = document.getElementById('insideTable');
        data.forEach(entry => {
            const row = document.createElement('tr');
            const userRow = document.createElement('td');
            const scoreRow = document.createElement('td');
            userRow.textContent = entry.screen_name;
            scoreRow.textContent = entry.high_score;
            row.appendChild(userRow);
            row.appendChild(scoreRow);
            insideTable.appendChild(row);
        });
    });
