'use strict'
const countryclue = document.querySelector('#questionname')
const playerguess = document.querySelector('#guess')


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

        console.log('taskarray: ', taskarray)
        console.log('questionsheetarray: ', questionsheetarray)

        const parsedquestionsheets = questionsheetarray.map(jsonStr => JSON.parse(jsonStr));
        const parsedtasks = taskarray.map(jsonStr => JSON.parse(jsonStr));

        parsedquestionsheets.forEach(obj => {
            console.log("Clue: ", obj.clue)
            console.log("A: ", obj.A)
            console.log("B: ", obj.B)
            console.log("C: ", obj.C)
        })

        parsedtasks.forEach(obj => {
            console.log("Task: ", obj.task)
            console.log("a: ", obj.a)
            console.log("b: ", obj.b)
            console.log("c: ", obj.c)
        })

    } catch (error) {
        console.log(error.message)
        }
}
sheetFunction()