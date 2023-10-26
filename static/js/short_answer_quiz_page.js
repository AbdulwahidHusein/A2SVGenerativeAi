let userAnswers = {}
        const cont = document.getElementById("quiz");
        const questionContainer = document.getElementById("question-container");
        const questionNumber = document.getElementById("question-number");
        const questionText = document.getElementById("question-text");
        const answerInput = document.getElementById("answer");
        const submitButton = document.getElementById("submit");
        const resultContainer = document.getElementById("result");
        const scoreValue = document.getElementById("score-value");

        let currentQuestionIndex = 0;
        let score = 0;

        function displayQuestion() {
            const question = quizData.questions[currentQuestionIndex];
            questionNumber.innerText = `Question ${currentQuestionIndex + 1}`;
            questionText.innerText = question;
            answerInput.value = "";
            questionContainer.classList.add("show");
        }
        function getFeedback(){
            document.getElementById('loader').style.display = 'block';
            var csrftoken = getCookie('csrftoken');
            var formData = new FormData();
            let answers = JSON.stringify(userAnswers)
            formData.append('submission', answers);

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                  if (!this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                  }
                }
              });
              
              $.ajax({
                type: 'POST',
                url: '/judge_short_answer_submission/',
                data: formData,
                processData: false,
                contentType: false,
                
                success: function(response) {
                  console.log(response.response);
                  let res = response.response;
                  document.getElementById('cont').style.display = "none";
                  explanationArea = document.getElementById("explanation-area");
                  explanationArea.style.display = 'flex'

                  for (var i=0; i<res.length; i++){
                    
                    var questionData = res[i];

                   
                    var questionDiv = document.createElement("div");
                    questionDiv.classList.add("questionn-container");
                
                    
                    var question = document.createElement("p");
                
                    question.classList.add("questionn");
                    question.textContent = questionData[0];
                
                
                    var userAnswer = document.createElement("p");
                    userAnswer.classList.add("user-answer");
                    userAnswer.textContent = "Your Answer: " + questionData[1];
                
               
                    var correctAnswer = document.createElement("p");
                    correctAnswer.classList.add("correct-answer");
                    correctAnswer.textContent = "Feed Back: " + questionData[2];
                
                  
                    questionDiv.appendChild(question);
                    questionDiv.appendChild(userAnswer);
                    questionDiv.appendChild(correctAnswer);
                
                 
                    explanationArea.appendChild(questionDiv);

                  }
                  console.log("score updated")
                  document.getElementById('loader').style.display = 'none';
                },
                error: function(xhr, status, error) {
                  console.log(error);
             
                }
              });
        }

        function saveAnswer() {
            const userAnswer = answerInput.value.trim().toLowerCase();
            userAnswers[quizData.questions[currentQuestionIndex]] = userAnswer
            const correctAnswer = "correct answer"; 

            if (userAnswer === correctAnswer) {
                score++;
            }

            currentQuestionIndex++;

            questionContainer.classList.remove("show");

            setTimeout(() => {
                if (currentQuestionIndex < quizData.questions.length) {
                    displayQuestion();
                } else {
                    showResult();
                    document.getElementById("judge-button").addEventListener(
                        'click', (event)=>{
                            getFeedback();
                        }
                    )
                }
            }, 300);
        }

        function showResult() {
            cont.style.display = "none";
            resultContainer.style.display = "block";
        }

        submitButton.addEventListener("click", saveAnswer);

        displayQuestion();


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