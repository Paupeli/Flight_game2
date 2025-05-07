'use strict'

    fetch("/scoreboard")
    .then(response => response.json())
    .then(data => {
        const insideTable = document.querySelector('#insideTable tbody');
        data.forEach(entry => {
            const row = document.createElement('tr')
            const userRow = document.createElement('td');
            const scoreRow = document.createElement('td');
            userRow.textContent = entry.user
            scoreRow.textContent = entry.score
            row.appendChild(userRow);
            row.appendChild(scoreRow);
            insideTable.appendChild(row);
        }
    )})
