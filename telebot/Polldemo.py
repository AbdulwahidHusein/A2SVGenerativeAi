from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import json


# Quiz data
quiz_data = """{'JS': [{'id': 1, 'question': 'What is the purpose of the Surface class?', 'options': ['To draw a 3D shape', 'To continuously redraw the scene', 'To specify Java 2D rendering hints', 'To increase the X-angle of the viewer'], 'answer': 'To continuously redraw the scene', 'score': 0, 'status': '', 'user_answer': '', 'explanation': 'The Surface class is used to continuously redraw the scene.'}, 
{'id': 2, 'question': 'What is the purpose of the RotatingGeometryUpdater class?', 'options': ['To draw a 3D shape', 'To continuously redraw the scene', 'To specify Java 2D rendering hints', 'To increase the X-angle of the viewer'], 'answer': 'To increase the X-angle of the viewer', 'score': 0, 'status': '', 'user_answer': '', 'explanation': 'The RotatingGeometryUpdater class is used to increase the X−angle of the viewer after each subsequent frame.'}, 
{'id': 3, 'question': 'What is the purpose of the MyJava3D class?', 'options': ['To draw a 3D shape', 'To continuously redraw the scene', 'To specify Java 2D rendering hints', 'To create an AwtRenderingEngine instance'], 'answer': 'To create an AwtRenderingEngine instance', 'score': 0, 'status': '', 'user_answer': '', 'explanation': 'The MyJava3D class creates an AwtRenderingEngine instance.'}, 
{'id': 4, 'question': 'What is the purpose of the ObjectFile class?', 'options': ['To draw a 3D shape', 'To continuously redraw the scene', 'To specify Java 2D rendering hints', 'To load a GeometryArray from disk'], 'answer': 'To load a GeometryArray from disk', 'score': 0, 'status': '', 'user_answer': '', 'explanation': 'The ObjectFile class is used to load a GeometryArray from disk.'}, 
{'id': 5, 'question': 'What is the purpose of the RenderingSurface class?', 'options': ['To draw a 3D shape', 'To continuously redraw the scene', 'To specify Java 2D rendering hints', 'To bind the rendering engine'], 'answer': 'To bind the rendering engine', 'score': 0, 'status': '', 'user_answer': '', 'explanation': 'The RenderingSurface class is used to bind the rendering engine.'}]}"""

# Parse the quiz data to Python object
quiz_data = json.loads(quiz_data)


# Quiz callback function
def start_quiz(update, context):
    quiz_questions = quiz_data["JS"]

    # Send the first question
    send_question(update, context, 0, quiz_questions)


def send_question(update, context, question_index, quiz_questions):
    question = quiz_questions[question_index]
    question_text = f"{question['question']}\n\n"

    # Generate inline keyboard markup for answer options
    options = question["options"]
    keyboard = [
        [
            InlineKeyboardButton(option, callback_data=f"{question_index}:{option}")
            for option in options
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the question and options
    update.message.reply_text(question_text, reply_markup=reply_markup)


def handle_answer(update, context):
    # Get the user's answer from the callback data
    query = update.callback_query
    question_index, user_answer = query.data.split(":")

    # Update the score and user's answer in the quiz data
    quiz_questions = quiz_data["JS"]
    question = quiz_questions[int(question_index)]
    question["user_answer"] = user_answer
    question["score"] = 1 if user_answer == question["answer"] else 0

    # Send the next question or end the quiz
    next_question_index = int(question_index) + 1
    if next_question_index < len(quiz_questions):
        send_question(update, context, next_question_index, quiz_questions)
    else:
        end_quiz(update, context, quiz_questions)


def end_quiz(update, context, quiz_questions):
    # Calculate the total score
    total_score = sum(question["score"] for question in quiz_questions)

    # Generate the final score message
    score_message = f"Quiz ended. Your score: {total_score}/{len(quiz_questions)}"

    # Send the final score message
    update.message.reply_text(score_message)
