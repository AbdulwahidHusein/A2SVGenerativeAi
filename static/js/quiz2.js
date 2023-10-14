
function test(shuffledQuestions){

//let shuffledQuestions = questionss//empty array to hold shuffled selected questions
length = shuffledQuestions.length
let correctAnswers = {}
let userAnswers = {}
let questionNumber = 0
let playerScore = 0  
let wrongAttempt = 0 
let indexNumber = 0

// function for displaying next question in the array to dom
function NextQuestion(index) {
    //handleQuestions()
        const currentQuestion = shuffledQuestions[index]
            document.getElementById("question-number").innerHTML = parseInt(index)+1 + " / "+ length
            document.getElementById("player-score").innerHTML = playerScore + " / "+ length
            document.getElementById("display-question").innerHTML = currentQuestion.question;
            document.getElementById("option-one-label").innerHTML = currentQuestion.optionA;
            document.getElementById("option-two-label").innerHTML = currentQuestion.optionB;
            document.getElementById("option-three-label").innerHTML = currentQuestion.optionC;
            document.getElementById("option-four-label").innerHTML = currentQuestion.optionD;
        }
   



function checkForAnswer() {
    const currentQuestion = shuffledQuestions[indexNumber] //gets current Question 
    const currentQuestionAnswer = currentQuestion.correctOption //gets current Question's answer
    const options = document.getElementsByName("option"); //gets all elements in dom with name of 'option' (in this the radio inputs)
    let correctOption = null

    options.forEach((option) => {
        //console.log(currentQuestion[option.value])
        //console.log(currentQuestionAnswer)
        if (option.value === currentQuestionAnswer) {
            //get's correct's radio input with correct answer
            
            correctOption = option.labels[0].id
        }
    })
   
    //checking to make sure a radio input has been checked or an option being chosen
    if (options[0].checked === false && options[1].checked === false && options[2].checked === false && options[3].checked == false) {
        document.getElementById('option-modal').style.display = "flex"
    }

    //checking if checked radio button is same as answer
    options.forEach((option) => {
        if (option.checked === true && option.value === currentQuestionAnswer) {
            document.getElementById(correctOption).style.backgroundColor = "green"
            correctAnswers[indexNumber] = 1
            userAnswers[indexNumber] = option.value
            playerScore++
            indexNumber++
            //set to delay question number till when next question loads
            setTimeout(() => {
                questionNumber++
            }, 1000)
        }

        else if (option.checked && option.value !== currentQuestionAnswer) {
            const wrongLabelId = option.labels[0].id
            document.getElementById(wrongLabelId).style.backgroundColor = "red"
            document.getElementById(correctOption).style.backgroundColor = "green"
            correctAnswers[indexNumber] = 0
            userAnswers[indexNumber] = option.value
            wrongAttempt++
            indexNumber++
            //set to delay question number till when next question loads
            setTimeout(() => {
                questionNumber++
            }, 1000)
        }
    })

}



//called when the next button is called
function handleNextQuestion() {
    if (indexNumber <= length-1) {

    checkForAnswer()
    unCheckRadioButtons()
    //delays next question displaying for a second
    setTimeout(() => {
        if (indexNumber <= length-1) {
            NextQuestion(indexNumber)
        }
        else {
            handleEndGame()
        }
        resetOptionBackground()
    }, 1000);
}
else{
    handleEndGame()
}
}

//sets options background back to null after display the right/wrong colors
function resetOptionBackground() {
    const options = document.getElementsByName("option");
    options.forEach((option) => {
        document.getElementById(option.labels[0].id).style.backgroundColor = ""
    })
}

// unchecking all radio buttons for next question(can be done with map or foreach loop also)
function unCheckRadioButtons() {
    const options = document.getElementsByName("option");
    for (let i = 0; i < options.length; i++) {
        options[i].checked = false;
    }
}

// function for when all questions being answered
function handleEndGame() {
    document.getElementsByClassName('game-quiz-container')[0].style.display = 'none'
    let remark = null
    let remarkColor = null

    // condition check for player remark and remark color
    if (playerScore <= length/3) {
        remark = "Bad Grades, Keep Practicing."
        remarkColor = "red"
    }
    else if (playerScore >= length/3 && playerScore < length*2/3) {
        remark = "Average Grades, You can do better."
        remarkColor = "orange"
    }
    else if (playerScore >= 2*length/3) {
        remark = "Excellent, Keep the good work going."
        remarkColor = "green"
    }
    const playerGrade = (playerScore / length) * 100

    //data to display to score board
    document.getElementById('remarks').innerHTML = remark
    document.getElementById('remarks').style.color = remarkColor
    document.getElementById('grade-percentage').innerHTML = playerGrade
    document.getElementById('wrong-answers').innerHTML = wrongAttempt
    document.getElementById('right-answers').innerHTML = playerScore
    document.getElementById('score-modal').style.display = "flex"
}

let explanationArea = document.getElementById('explanations')

function showExplanation() {
    document.getElementsByClassName('main')[0].style.display = 'none';
    let explanationArea = document.getElementById('explanations');
    explanationArea.innerHTML += "this is for the test "
    //console.log(correctAnswers)
    console.log(shuffledQuestions)
    
    for (let [key, value] of Object.entries(correctAnswers)) {
        if (value == 1 || value == '1') {
            explanationArea.innerHTML += 
            '<div class="single-result correct-answer">' +
            '<p class="explanation-question"><h>Question ' + (parseInt(key) + 1) + ': </h>' + shuffledQuestions[key].question + '</p>'
            + '<p class="explanation-correctAnswer"><h> Correct Answer: </h>' + shuffledQuestions[key][shuffledQuestions[key].correctOption] + '</p>'+
            '<p class="explanation-correctAnswer"><h> Explanation:</h> ' + shuffledQuestions[key].explanation + ' </p>' +
            '</div>'
        } else {
            let query = 'Provide me Explanation about the following question ' + shuffledQuestions[key].question;
            query += ' and the choices are ' + ' ' + shuffledQuestions[key].optionA + ' ' + shuffledQuestions[key].optionB + ' ' + shuffledQuestions[key].optionC + ' ' + shuffledQuestions[key].optionD + ' what is the correct answer and tell me the reason';
            query += ' and some user answered this question as '+ shuffledQuestions[key][userAnswers[key]] +' explain him why the he is wrong and what may be his approach'
            explanationArea.innerHTML +=
                '<div class="single-result">' +
                '<p class="explanation-question"><h>Question ' + (parseInt(key) + 1) + ':</h> ' + shuffledQuestions[key].question + '</p>' +
                '<p class="explanation-correctAnswer"><h> Your Answer:</h> ' + shuffledQuestions[key][userAnswers[key]] + '</p>' +
                '<p class="explanation-correctAnswer"><h> Correct Answer:</h> ' + shuffledQuestions[key][shuffledQuestions[key].correctOption] + '</p>' +
                '<p class="explanation-correctAnswer"><h> Explanation:</h> ' + shuffledQuestions[key].explanation + ' </p>' +
                `<a class="more-exp-link" href="chat/${query}" >More Explanations </a>` +
                '</div>';
        }
    }
}

//closes score modal and resets game
function closeScoreModal() {
    questionNumber = 0
    playerScore = 0
    wrongAttempt = 0
    indexNumber = 0
    //shuffledQuestions = []
    NextQuestion(indexNumber)
    document.getElementById('score-modal').style.display = "none"
}

//function to close warning modal
function closeOptionModal() {
    //explanationArea.style.display = 'block'
    document.getElementById('option-modal').style.display = "none"
}
document.addEventListener('DOMContentLoaded', function() {
document.getElementById('next').addEventListener('click', handleNextQuestion)
document.getElementById('exp-btn').addEventListener('click', showExplanation)
document.getElementById('close-modal-btn').addEventListener('click', closeOptionModal)
NextQuestion(0);
})


}