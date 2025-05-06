'use strict'
const countryclue = document.querySelector('#questionname')
const playerguess = document.querySelector('#guess')
const a = document.querySelector('#A')
const b = document.querySelector('#B')
const c = document.querySelector('#C')
const scoredisplay = document.querySelector('#score')
const wronganswerdisplay = document.querySelector('#wronganswers')
const questionnumberdisplay = document.querySelector('#question_num')
let feedback = document.querySelector('#feedback')


async function sheetFunction() {
    console.log('Fetching..')
    try {
        const response = await fetch(`http://127.0.0.1:3000/flight_game/5`)
        const jsondata = await response.json()

        console.log('All Data:', jsondata)
        console.log('Questionsheets', jsondata.questionsheets)
        console.log('Tasks', jsondata.Tasks)

        const questionsheetarray = jsondata.questionsheets
        const taskarray = jsondata.Tasks
        const mult = jsondata.mult
        let score = 0
        let wronganswers = 0


        console.log('taskarray: ', taskarray)
        console.log('questionsheetarray: ', questionsheetarray)

        const parsedquestionsheets = questionsheetarray.map(jsonStr => JSON.parse(jsonStr));
        const parsedtasks = taskarray.map(jsonStr => JSON.parse(jsonStr));

        let currentquestionindx = 0
        function displayCurrentQuestion() {
            if (currentquestionindx < parsedquestionsheets.length) {
                const question = parsedquestionsheets[currentquestionindx]
                countryclue.textContent = question.clue
                a.textContent = question.a
                b.textContent = question.b
                c.textContent = question.c
                enableButtons(true);
                let questionnum = currentquestionindx+1
                let questionnum_str = toString(questionnum)
                questionnumberdisplay.textContent = questionnum_str


            } else {
            window.location.href ="Python/templates/finish.html"
                }
            }

        function nextQuestion() {
            currentQuestionIndex++;
            displayCurrentQuestion();
        }

        function enableButtons(enabled) {
            document.querySelectorAll('#guess button').forEach(btn => {
            btn.disabled = !enabled;
        });
        }

        function checkAnswer(selected) {
            enableButtons(false)
            const currentQuestion = parsedquestionsheets[currentquestionindx]
            const answer = currentQuestion.answer
            if (selected === answer) {
                score = score+(100*mult)
                const task = parsedtasks[currentquestionindx]
                countryclue.textContent = task.task
                a.textContent = task.a
                b.textContent = task.b
                c.textContent = task.c
                enableButtons(true);

            }
            else {
                score = score-(50*mult)
                wronganswers++

            }
        }



        parsedtasks.forEach(obj => {
            console.log("Task: ", obj.task)
            console.log("a: ", obj.a)
            console.log("b: ", obj.b)
            console.log("c: ", obj.c)
        })

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


    } catch (error) {
        console.log(error.message)
        }
}
sheetFunction()