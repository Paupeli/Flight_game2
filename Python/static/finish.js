'use strict';

const user = localStorage.getItem("username");
const score = Number(localStorage.getItem("finalScore"));

if (user && !isNaN(score)) {
  saveScore(user, score);
} else {
  console.error("Missing username or score in localStorage.");
}

//tallentaa scoren
function saveScore(user, score) {
  fetch(`/flight_game/scoreboard/save_score/${user}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ score: score })  // Send the score as JSON
  })
  .then(response => response.json())
  .then(data => {
    if (data.new_high_score) {
      alert(`Congratulations! You got a new high score: ${score} points!`);
    }
  })
  .catch(error => {
    console.error("Error saving score:", error);
  });
}

document.getElementById("quit-btn").addEventListener("click", () => {
  window.location.href = "/start"; //byeee
});

document.getElementById("main_menu-btn").addEventListener("click", () => {
  window.location.href = "/main_menu"; //main menuun menee tämä
})

document.getElementById("scoreboard-btn").addEventListener("click", () => {
  window.location.href = "/scoreboard"; //scoreboardiin
})