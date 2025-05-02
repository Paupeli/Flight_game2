'use strict'
const countryclue = document.querySelector('#questionname')
const playerguess = document.querySelector('#guess')
const questionsheetarray = []
const taskarray = []

async function sheetFunction() {
    console.log('Fetching..')
    try {
        const response = await fetch(`http://127.0.0.1:3000/flight_game/5`)
        const jsondata = await response.json()
        console.log('All Data:', jsondata)
        for (const data of jsondata) {
            questionsheetarray.push(data.questionsheets)
            taskarray.push(data.tasks)
        }
        console.log('Tasks: ', taskarray)
        console.log('Questionsheets: ', questionsheetarray)
    } catch (error) {
        console.log(error.message)
        }
}
sheetFunction()