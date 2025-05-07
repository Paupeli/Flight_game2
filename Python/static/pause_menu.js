'use strict';

let isGamePaused = true;
const continueButton = document.getElementById('btn-continue');
const pauseMenu = document.getElementById('pause-menu');

//linkittyy oikeisiin paikkoihin
document.getElementById('btn-main-menu').addEventListener('click', goToMainMenu);
document.getElementById('btn-scoreboard').addEventListener('click', showScoreboard);
document.getElementById('btn-rules').addEventListener('click', showRules);
document.getElementById('btn-quit').addEventListener('click', quitGame);

//jatkaa peliä
continueButton.addEventListener('click', () => {
    continueGame();
});

function pauseGame() {
    isGamePaused = true;
    pauseMenu.classList.remove('hidden');
}

function continueGame() {
    isGamePaused = false;
    pauseMenu.classList.add('hidden');
}

function goToMainMenu() {
    window.location.href = "/main_menu";
}

function showScoreboard() {
    window.location.href = "/scoreboard";
}

function showRules() {
    window.location.href = "/rules";
}

function quitGame() {
    window.location.href = "/";
}
