'use strict'
const countryclue = document.querySelector('#questionname')
const A = document.querySelector('#A')
const B = document.querySelector('#B')
const C = document.querySelector('#C')
const scoredisplay = document.querySelector('#score')
const wronganswerdisplay = document.querySelector('#wronganswers')
const questionnumberdisplay = document.querySelector('#question_num')
let feedback = document.querySelector('#feedback')


async function sheetFunction() {
    console.log('Fetching..')
    try {
        const gameLength = localStorage.getItem('gameLength');
        const username = localStorage.getItem('username');
        const response = await fetch(`http://127.0.0.1:3000/createroute/10`)
        const jsondata = await response.json()

        console.log('All Data:', jsondata)
        console.log('Questionsheets', jsondata.questionsheets)
        console.log('Tasks', jsondata.Tasks)

        const questionsheetarray = jsondata.questionsheets
        const taskarray = jsondata.Tasks
        const mult = parseInt(jsondata.Mult)
        let score = 0
        let gainedscore = 0
        let wronganswers = 0
        let lastanswercorrect = false
        scoredisplay.textContent = "Score: " + score
        wronganswerdisplay.textContent = "Wrong answers: " + wronganswers

        let isInTasks = false


        console.log('taskarray: ', taskarray)
        console.log('questionsheetarray: ', questionsheetarray)
        console.log('jsonmult: ', jsondata.Mult)
        console.log('mult: ', mult)


        const parsedquestionsheets = questionsheetarray.map(jsonStr => JSON.parse(jsonStr));
        const parsedtasks = taskarray.map(jsonStr => JSON.parse(jsonStr));
        console.log(parsedquestionsheets)
        console.log(parsedtasks)

        let currentquestionindx = 0
        function displayCurrentQuestion() {
            if (!isInTasks && currentquestionindx < parsedquestionsheets.length && wronganswers < 3) {
                const question = parsedquestionsheets[currentquestionindx]
                countryclue.textContent = question.clu
                A.textContent = question.A
                B.textContent = question.B
                C.textContent = question.C
                feedback.textContent = ""
                enableButtons(true)
                let questionnum = currentquestionindx + 1
                let questionnum_str = questionnum.toString()
                questionnumberdisplay.textContent = "Current question: " + questionnum_str
            } else if (isInTasks && currentquestionindx < parsedquestionsheets.length && wronganswers < 3) {
                const question = parsedtasks[currentquestionindx]
                countryclue.textContent = question.task
                A.textContent = question.a
                B.textContent = question.b
                C.textContent = question.c
                feedback.textContent = ""
                enableButtons(true)
            }

            else {
            localStorage.setItem('finalScore', score);
            localStorage.setItem('username', username);
            window.location.href =("/new_game/finish")
                }
            }

        function nextQuestion() {
            if (isInTasks) {
                isInTasks = false
                displayCurrentQuestion()
            } else {
                currentquestionindx++
                if (lastanswercorrect) {
                    isInTasks = true
                    displayCurrentQuestion()
                } else {
                    displayCurrentQuestion()
                }
            }
        }

        function enableButtons(enabled) {
            document.querySelectorAll('#guess button').forEach(btn => {
            btn.disabled = !enabled;
        });
        }

        function checkAnswer(selected) {
            enableButtons(false)

            if (!isInTasks) {
                const currentQuestion = parsedquestionsheets[currentquestionindx]
                const answer = currentQuestion.answer
                if (selected === answer) {
                    gainedscore = 100*mult
                    score = score+gainedscore

                    feedback.textContent = "Correct, you got" + gainedscore + "points"
                    lastanswercorrect = true
                    scoredisplay.textContent = "Score: " + score
                } else if (selected !== answer) {
                    gainedscore = 50*mult
                    score = score-gainedscore

                    feedback.textContent = "Oh no, you lost " + gainedscore + "points"
                    wronganswers++
                    scoredisplay.textContent = "Score: " + score
                    lastanswercorrect = false
                    let wronganswersstr = wronganswers.toString()
                    wronganswerdisplay.textContent = "Wrong answers: " + wronganswersstr
                }

            } else {
                const currentQuestion = parsedtasks[currentquestionindx]
                const answer = currentQuestion.correct_answer
                if (selected === answer && isInTasks) {
                    gainedscore = 50*mult
                    feedback.textContent = "Correct, you got "+ gainedscore + "points"
                    score = score+gainedscore
                    scoredisplay.textContent = "Score: " + score
                } else {
                    gainedscore = 25*mult

                    feedback.textContent = "Oh no, you lost "+ gainedscore + "points"
                    score = score-gainedscore
                    scoredisplay.textContent = "Score: " + score
                }}
            setTimeout(nextQuestion, 2000)
        }


        document.getElementById('A').addEventListener('click', function(e) {
            e.preventDefault(); // Prevent form submission
            checkAnswer('A');
        });

        document.getElementById('B').addEventListener('click', function(e) {
            e.preventDefault(); // Prevent form submission
            checkAnswer('B');
        });

        document.getElementById('C').addEventListener('click', function(e) {
            e.preventDefault(); // Prevent form submission
            checkAnswer('C');
        });

        enableButtons(false)
        displayCurrentQuestion()


    } catch (error) {
        console.log(error.message)
        }
}
sheetFunction()