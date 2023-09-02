function test(quiz){

    var quizApp = function () {
  
    this.score = 0;
    this.qno = 1;
    this.currentque = 0;
    var totalque = quiz['JS'].length;
  
    this.displayQuiz = function (cque) {
    this.currentque = cque;
  
    if (this.currentque < totalque) {
    $("#tque").html(totalque);
    $("#previous").attr("disabled", false);
    $("#next").attr("disabled", false);
    $("#qid").html(quiz.JS[this.currentque].id + '.');
    $("#question").html(quiz.JS[this.currentque].question);
    $("#question-options").html("");
  
    var choices = ["A. ", "B. ","C. ", "D. "]
    for (var i =0; i <  quiz.JS[this.currentque].options.length; i++) {
    $("#question-options").append(
    "<div class='form-check option-block'>" +
    "<label class='form-check-label'>" +
    "<input type='radio' class='form-check-input' name='option' style='color:white' id='q" + choices[i] + "' value='" + quiz.JS[this.currentque].options[i] + "'><span id='optionval' >" +
    quiz.JS[this.currentque].options[i] +
    "</span></label>"
    );
    }
    }
  
    if (this.currentque <= 0) {
    $("#previous").attr("disabled", true);
    }
  
  
    if (this.currentque >= totalque) {
    $('#next').attr('disabled', true);
    for (var i = 0; i < totalque; i++) {
    this.score = this.score + parseInt(quiz.JS[i].score);
    }
    return this.showResult(this.score);
    }
  
    }
  
  
    this.showResult = function (scr) {
    $("#result").addClass('result');
    $("#result").html("<h1 class='res-header'>Total Score: &nbsp;" + scr + '/' + totalque + "</h1>");
    for (var j = 0; j < totalque; j++) {
    var res;
    if (quiz.JS[j].score == 0) {
    res = '<span class="wrong"> you are Wrong</span><i class="fa fa-remove c-wrong"></i>';
    } else {
    res = '<span class="correct">You are correct</span><i class="fa fa-check c-correct"></i>';
    }
    $("#result").append(
    '<div class="result-question"><span>Question ' + quiz.JS[j].id + '</span> &nbsp;' + quiz.JS[j].question + '</div>' +
  
    '<div><b>Your answer:</b> &nbsp;' + quiz.JS[j].user_answwer + '</div>' +
    '<div><b>Correct answer:</b> &nbsp;' + quiz.JS[j].answer + '</div>' +
  
    '<div class="result-question"><span>Explanation ' + quiz.JS[j].id + '</span> &nbsp;' + quiz.JS[j].explanation + '</div>' +
  
    '<div class="last-row"><b></b> &nbsp;' + res +
    '</div>'
    );
    }
    }
    this.checkAnswer = function (option) {
    var answer = quiz.JS[this.currentque].answer;
    option = option.replace(/</g, "&lt;") //for <
    option = option.replace(/>/g, "&gt;") //for >
    option = option.replace(/"/g, "&quot;")
    if (option == quiz.JS[this.currentque].answer) {
    if (quiz.JS[this.currentque].score == "") {
    quiz.JS[this.currentque].score = 1;
    quiz.JS[this.currentque].status = "correct";
    }
    } else {
    quiz.JS[this.currentque].status = "wrong";
    }
    quiz.JS[this.currentque].user_answwer = option;
    }
    this.changeQuestion = function (cque) {
    this.currentque = this.currentque + cque;
    this.displayQuiz(this.currentque);
    }
    }
  
    var jsq = new quizApp();
    var selectedopt;
    $(document).ready(function () {
    jsq.displayQuiz(0);
    $('#question-options').on('change', 'input[type=radio][name=option]', function (e) {
    //var radio = $(this).find('input:radio');
    $(this).prop("checked", true);
    selectedopt = $(this).val();
    });
    });
    $('#next').click(function (e) {
    e.preventDefault();
    if (selectedopt) {
    jsq.checkAnswer(selectedopt);
    }
    jsq.changeQuestion(1);
    });
    $('#previous').click(function (e) {
    e.preventDefault();
    if (selectedopt) {
    jsq.checkAnswer(selectedopt);
    }
    jsq.changeQuestion(-1);
    });
  
  }
  
  