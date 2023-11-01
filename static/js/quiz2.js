let correctAnswers = {}
let qs = {}
let userAnswers = {}
function test(shuffledQuestions, QuizId){
    qs = shuffledQuestions;
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

//let shuffledQuestions = questionss//empty array to hold shuffled selected questions
length = shuffledQuestions.length

let questionNumber = 0
let playerScore = 0  
let wrongAttempt = 0 
let indexNumber = 0

// function for displaying next question in the array to dom
function NextQuestion(index) {
    closeOptionModal()
    if (groupQuiz){
        var csrftoken = getCookie('csrftoken');
        var formData = new FormData();
        formData.append('id', groupId);
        formData.append('score', playerScore);
        
     // Add CSRF token to request headers
     $.ajaxSetup({
       beforeSend: function(xhr, settings) {
         if (!this.crossDomain) {
           xhr.setRequestHeader('X-CSRFToken', csrftoken);
         }
       }
     });
     
     $.ajax({
       type: 'POST',
       url: '/update_scoreboard/',
       data: formData,
       processData: false,
       contentType: false,
       success: function(response) {
         console.log(response);
         // Handle the success response here
       },
       error: function(xhr, status, error) {
         console.log(error);
         // Handle the error response here
       }
     });
    }
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
        document.getElementById('option-modal').style.visibility = "visible"
    }

    //checking if checked radio button is same as answer
    options.forEach((option) => {
        console.log(option.value + ' ' + currentQuestionAnswer )
        if (option.checked === true && option.value == currentQuestionAnswer) {
            // document.getElementById(correctOption).style.backgroundColor = "green"
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
            // document.getElementById(wrongLabelId).style.backgroundColor = "red"
            // document.getElementById(correctOption).style.backgroundColor = "green"
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

    //send ajax request
    //use QuizId
   // Retrieve the CSRF token from the Django template
   var csrftoken = getCookie('csrftoken');
   var formData = new FormData();
   formData.append('id', QuizId);
   formData.append('score', playerScore);
   
// Add CSRF token to request headers
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!this.crossDomain) {
      xhr.setRequestHeader('X-CSRFToken', csrftoken);
    }
  }
});

$.ajax({
  type: 'POST',
  url: '/update_quiz/',
  data: formData,
  processData: false,
  contentType: false,
  success: function(response) {
    console.log(response);
    // Handle the success response here
  },
  error: function(xhr, status, error) {
    console.log(error);
    // Handle the error response here
  }
});


    }
    //update_scoreboard

function showExplanation() {
    document.getElementsByClassName('main')[0].style.display = 'none';
    let explanationArea = document.getElementById('explanations');
    explanationArea.style.display = 'block';

    // //console.log(correctAnswers)
    // //console.log(shuffledQuestions)
    
    // for (let [key, value] of Object.entries(correctAnswers)) {
    //     let query = 'Provide me Explanation about the following question ' + shuffledQuestions[key].question;
    //         query += ' and the choices are ' + ' ' + shuffledQuestions[key].optionA + ' ' + shuffledQuestions[key].optionB + ' ' + shuffledQuestions[key].optionC + ' ' + shuffledQuestions[key].optionD + ' what is the correct answer and tell me the reason';
    //         query += ' and I answered this question as '+ shuffledQuestions[key][userAnswers[key]] +' explain me why I am wrong and what may be the reason that me conclude this and what should I always remember'

    //     if (value == 1 || value == '1') {
    //         explanationArea.innerHTML += 
    //         '<div class="single-result  border border-primary rounded p-3 mt-3">' +
    //         '<p class="exp explanation-question"><h>Question ' + (parseInt(key) + 1) + ': </h>' + shuffledQuestions[key].question + '</p>'
    //         + '<p class="exp explanation-correctAnswer"><h> Correct Answer: </h>' + shuffledQuestions[key][shuffledQuestions[key].correctOption] + '</p>'+
    //         '<p class="exp explanation-correctAnswer"><h> Explanation:</h> ' + shuffledQuestions[key].explanation + ' </p>' +
    //         '</div>'
    //     } else {
            
    //         explanationArea.innerHTML +=
    //         `<div class="single-result border border-primary rounded p-3 mt-3">
    //             <p class="exp explanation-question"><h>Question ${parseInt(key) + 1}:</h> ${shuffledQuestions[key].question}</p>
    //             <p class="exp explanation-correctAnswer"><h> Your Answer:</h> ${shuffledQuestions[key][userAnswers[key]]}</p>
    //             <p class="exp explanation-correctAnswer"><h> Correct Answer:</h> ${shuffledQuestions[key][shuffledQuestions[key].correctOption]}</p>
    //             <p class="exp explanation-correctAnswer"><h> Explanation:</h> ${shuffledQuestions[key].explanation}</p>
    //             <form action="{% url 'get_chat' %}" method="post">{% csrf_token %} <input name="query" value="${ query }" type="hidden"><button type="submit">View More Explanations</button></form>
    //         </div>`;
    //     }
    //}
}
//`<a class="more-exp-link" href="http://127.0.0.1:8000/chat/?query=${query}"  target="_blank" >More Explanations </a>`
//function to close warning modal
function closeOptionModal() {
    //explanationArea.style.display = 'block'
    document.getElementById('option-modal').style.visibility = "hidden"
}
document.addEventListener('DOMContentLoaded', function() {
document.getElementById('next').addEventListener('click', handleNextQuestion)
document.getElementById('exp-btn').addEventListener('click', showExplanation)
NextQuestion(0);
})


}
function getQuery(question){
    
    var index = qs.findIndex(function(q) {
        return q.question === question;
      });

    let query = "";
    if (userAnswers[index] === '1'){
        query += 'Provide me a more detailed Explanation about the following question question: ' + qs[index].question;
        query += ' and the choices are ' + ' ' + qs[index].optionA + ' ' + qs[index].optionB + ' ' + qs[index].optionC + ' ' + qs[index].optionD + ' I have answered the question correctely again tell me additional explanations';
        query += ' My answer was '+ qs[index][userAnswers[index]] +' based on this justify my answer. '
    }
    else{
        query += 'Provide me Explanation about the following question question: ' + qs[index].question;
        query += ' and the choices are ' + ' ' + qs[index].optionA + ' ' + qs[index].optionB + ' ' + qs[index].optionC + ' ' + qs[index].optionD + ' what is the correct answer and tell me the reason';
        query += ' and our I answered this question as '+ qs[index][userAnswers[index]] +' explain weather I am are right or wrong. and if wrong what may be the reason that made me the answer like this. what should they always remember'
    }
   
    return query
}