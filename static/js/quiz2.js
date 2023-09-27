const questions = [
    {
      question: "Which law of thermodynamics states that energy cannot be created or destroyed, only transferred or transformed?",
      optionA: "First Law of Thermodynamics",
      optionB: "Second Law of Thermodynamics",
      optionC: "Third Law of Thermodynamics",
      optionD: "Zeroth Law of Thermodynamics",
      correctOption: "optionA",
      explanation: "The First Law of Thermodynamics, also known as the Law of Energy Conservation, states that energy is conserved in any thermodynamic process."
    },
    {
      question: "Which law of thermodynamics states that the total entropy of an isolated system always increases over time?",
      optionA: "First Law of Thermodynamics",
      optionB: "Second Law of Thermodynamics",
      optionC: "Third Law of Thermodynamics",
      optionD: "Zeroth Law of Thermodynamics",
      correctOption: "optionB",
      explanation: "The Second Law of Thermodynamics states that the entropy of an isolated system tends to increase over time, leading to the concept of irreversibility in nature."
    },
    {
      question: "Which law of thermodynamics defines the concept of absolute zero?",
      optionA: "First Law of Thermodynamics",
      optionB: "Second Law of Thermodynamics",
      optionC: "Third Law of Thermodynamics",
      optionD: "Zeroth Law of Thermodynamics",
      correctOption: "optionC",
      explanation: "The Third Law of Thermodynamics states that as the temperature approaches absolute zero, the entropy of a pure, perfect crystal approaches zero."
    },
    {
      question: "Which law of thermodynamics states that if two systems are each in thermal equilibrium with a third system, then they are in thermal equilibrium with each other?",
      optionA: "First Law of Thermodynamics",
      optionB: "Second Law of Thermodynamics",
      optionC: "Third Law of Thermodynamics",
      optionD: "Zeroth Law of Thermodynamics",
      correctOption: "optionD",
      explanation: "The Zeroth Law of Thermodynamics establishes the concept of temperature and thermal equilibrium."
    },
    {
      question: "Which process involves the transfer of heat energy through direct physical contact between particles?",
      optionA: "Conduction",
      optionB: "Convection",
      optionC: "Radiation",
      optionD: "Evaporation",
      correctOption: "optionA",
      explanation: "Conduction is the process of heat transfer between objects or substances in direct physical contact."
    },
    {
      question: "Which process involves the transfer of heat energy through the movement of fluid or gas particles?",
      optionA: "Conduction",
      optionB: "Convection",
      optionC: "Radiation",
      optionD: "Evaporation",
      correctOption: "optionB",
      explanation: "Convection occurs when heat is transferred through the bulk movement of a fluid or gas."
    },
    {
      question: "Which process involves the transfer of heat energy through electromagnetic waves?",
      optionA: "Conduction",
      optionB: "Convection",
      optionC: "Radiation",
      optionD: "Evaporation",
      correctOption: "optionC",
      explanation: "Radiation is the transfer of heat energy through electromagnetic waves, such as infrared radiation."
    },
    {
      question: "Which process involves the phase change of a liquid into a gas at the surface of the liquid?",
      optionA: "Conduction",
      optionB: "Convection",
      optionC: "Radiation",
      optionD: "Evaporation",
      correctOption: "optionD",
      explanation: "Evaporation is the process by which a liquid changes into a gas at the surface, typically due to heat energy."
    },
    {
      question: "Which process involves the phase change of a gas into a liquid?",
      optionA: "Condensation",
      optionB: "Melting",
      optionC: "Sublimation",
      optionD: "Freezing",
      correctOption: "optionA",
      explanation: "Condensation is the process by which a gas changes into a liquid, typically due to cooling or compression."
    },
    {
      question: "Which process involves the phase change of a solid directly into a gas without passing through the liquid phase?",
      optionA: "Condensation",
      optionB: "Melting",
      optionC: "Sublimation",
      optionD: "Freezing",
      correctOption: "optionC",
      explanation: "Sublimation is the process by which a solid changes directly into a gas without becoming a liquid first."
    },
  ];



let shuffledQuestions = questions//empty array to hold shuffled selected questions
length = questions.length
/*
function handleQuestions() { 
    //function to shuffle and push 10 questions to shuffledQuestions array
    while (shuffledQuestions.length <= 9) {
        const random = questions[Math.floor(Math.random() * questions.length)]
        if (!shuffledQuestions.includes(random)) {
            shuffledQuestions.push(random)
        }
    }
}*/
let correctAnswers = {}
let userAnswers = {}
let questionNumber = 1
let playerScore = 0  
let wrongAttempt = 0 
let indexNumber = 0

// function for displaying next question in the array to dom
function NextQuestion(index) {
    //handleQuestions()
    if (indexNumber <length){
        const currentQuestion = shuffledQuestions[index]
        document.getElementById("question-number").innerHTML = questionNumber + " / "+ length
        document.getElementById("player-score").innerHTML = playerScore + " / "+ length
        document.getElementById("display-question").innerHTML = currentQuestion.question;
        document.getElementById("option-one-label").innerHTML = currentQuestion.optionA;
        document.getElementById("option-two-label").innerHTML = currentQuestion.optionB;
        document.getElementById("option-three-label").innerHTML = currentQuestion.optionC;
        document.getElementById("option-four-label").innerHTML = currentQuestion.optionD;
    
    }
   
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
    else if (playerScore >= length/2 && playerScore < length*2/3) {
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
function showExplanation(){
document.getElementsByClassName('main')[0].style.display = 'none'
let explanationArea = document.getElementById('explanations')

    for (let [key, value] in Object.entries(correctAnswers)){
        if (value == 1 || value =='1'){
            explanationArea.innerHTML += '<p class="explanation-question"><h>Question ' +parseInt(key)+1 + ': </h>'+ questions[key].question +'</p>'
            explanationArea.innerHTML += '<p class="explanation-correctAnswer"><h> Correct Answer: </h>' + questions[key][questions[key].correctOption] +'</p>'
        }
        else{
        let query = 'Provide me Explanation about the following question ' + questions[key].question
       query +=  ' and the choices are '+ ' '+questions[key].optionA+' '+questions[key].optionB + ' '+questions[key].optionC +' '+questions[key].optionD + 'what is the correct answer and tell me the reason '
        explanationArea.innerHTML += 
        '<div class="single-result">'+
        '<p class="explanation-question"><h>Question '+parseInt(key)+':</h> '+ questions[key].question +'</p>'
     + '<p class="explanation-correctAnswer"><h> Your Answer:</h> ' + questions[key][userAnswers[key]] +'</p>'
       + '<p class="explanation-correctAnswer"><h> Correct Answer:</h> ' + questions[key][questions[key].correctOption] +'</p>'
         + '<p class="explanation-correctAnswer"><h> Explanation:</h> '+ questions[key].explanation + ' </p>'
         + `<a class="more-exp-link" href="chat/${query}" >More Explanations </a>`
    }
    }
}

//closes score modal and resets game
function closeScoreModal() {
    questionNumber = 1
    playerScore = 0
    wrongAttempt = 0
    indexNumber = 0
    shuffledQuestions = []
    NextQuestion(indexNumber)
    document.getElementById('score-modal').style.display = "none"
}

//function to close warning modal
function closeOptionModal() {
    //explanationArea.style.display = 'block'
    document.getElementById('option-modal').style.display = "none"
}

