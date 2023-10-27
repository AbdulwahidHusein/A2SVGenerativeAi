import json
import logging
import os
import openai
import sys
import time
import request

sys.path.append("..")
from telegram import (
    Bot,
    Message,
    ChatAction,
    Poll,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    File,
    PollAnswer,
)
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    Updater,
    CallbackQueryHandler,
    PollAnswerHandler,
)
from dotenv import load_dotenv


load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")
TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# some global variables for storing data.
user_data = {}
question_format = {}
user_answers = {}
scores = {}
START_PAGE = 0
END_PAGE = 1
poll_ids = []
poll_message_id = []


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter file")


# The start function
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello There, please enter file so we can change it to qize for you!"
    )


# displays the difficulty buttons
def set_difficulty(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Easy", callback_data="easy")],
        [InlineKeyboardButton("Medium", callback_data="medium")],
        [InlineKeyboardButton("Difficult", callback_data="difficult")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose Difficulty:", reply_markup=reply_markup)


# function for setting the end page of the recieved file
def set_end(update: Update, context: CallbackContext):
    end = update.message.text
    user_data["end_page"] = int(end)
    update.message.reply_text(
        f"Start page: {user_data['start_page']}\nEnd page: {user_data['end_page']}"
    )
    set_difficulty(update=update, context=context)


# function for setting the start page of the received file
def set_start(update: Update, context: CommandHandler):
    start = update.message.text
    user_data["start_page"] = int(start)
    update.message.reply_text("Enter end page")
    return END_PAGE


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END


# Function for processing the file. It works by downloading the file first and then moves on to processing it.
def Enterfile(update: Update, context: CallbackContext):
    try:
        global user_data
        file = update.message.document
        file_recieved = context.bot.get_file(file_id=file.file_id)
        file_name = file.file_name
        store = file_name.split(".")
        if store[-1] != "pdf":
            raise Exception
        user_data["file_name"] = file_name
        file_downloaded = file_recieved.download()
        user_data["file"] = file_downloaded
        with open(file_downloaded, "rb") as f:
            user_data["file"] = file_downloaded

        reply_text = f"Recieved file: {user_data['file_name']}"
        user_data["file_name"] = file_name
        context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=reply_text + "\nEnter start page:",
        )
        return START_PAGE
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="please upload a valid pdf file"
        )


# this function handles the events that happen when a button is pressed
def button_callback(update: Update, context: CallbackContext):
    global user_data
    global difficulty
    query = update.callback_query
    if query.data == "easy" or query.data == "medium" or query.data == "difficult":
        user_data["difficulty"] = query.data
        query.message.reply_text(
            f"diffiiculty set to {user_data['difficulty']}\nPlease wait till we generate the quiz...",
        )
        send_request(update=update, context=context)


# function for sending explanation.
def send_explanation(update: Update, context: CallbackContext):
    try:
        result_message = "Here are the explanations:\n"

        for i, question_data in enumerate(question_format["questions"]):
            result_message += f"Question {i + 1}: {question_data['question']}\n"

            result_message += f"Explanation: {question_data['explanation']}\n\n"

        context.bot.send_message(chat_id=update.effective_chat.id, text=result_message)
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="No Explanation found. please upload file to generate quiz first",
        )


# this function handles the answers when a poll is selected. it increments each user's score if it is correct
def poll_answer_handler(update: Update, context: CallbackContext):
    answer: PollAnswer = update.poll_answer
    try:
        # Check if the user's answer is correct
        print(answer, "hi", answer.option_ids[0])
        print(user_answers, "user hi")
        print(user_answers[answer.poll_id][-1], ord(user_answers[answer.poll_id][-1]))
        print(
            answer.option_ids[0],
            ord(user_answers[answer.poll_id][-1]) - ord("A"),
            answer.option_ids[0] == ord(user_answers[answer.poll_id][-1]) - ord("A"),
        )
        if answer.option_ids[0] == ord(user_answers[answer.poll_id][-1]) - ord("A"):
            user_id = answer.user.id
            scores[user_id] = scores.get(user_id, 0) + 1
        else:
            scores[user_id] = scores.get(user_id, 0)
    except:
        pass


# function for sending the rank of each user
def send_rankings(update: Update, context: CallbackContext):
    print(scores)
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    # Calculate rankings based on scores dictionary
    ranked_users = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Send rankings message
    rankings_message = "Rankings:\n"
    for rank, (user_id, score) in enumerate(ranked_users, start=1):
        user = context.bot.get_chat_member(
            chat_id=update.effective_chat.id, user_id=user_id
        ).user
        rankings_message += f"{rank}. {user.username or user.full_name}: {score}\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=rankings_message)


# function for generating question and sending the generating question in a quiz poll format for users
# it calls the send explanation function 20 seconds after the final poll is sent
def send_request(update: Update, context: CallbackContext):
    global user_data
    global question_format
    polls_sent_count = 0
    total_polls = 0

    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    question_format = request.send_request_(
        user_data["file"],
        user_data["start_page"],
        user_data["end_page"],
        user_data["difficulty"],
    )
    logging.info("request sent")
    total_polls = len(question_format["questions"]) - 1
    for i, question_data in enumerate(question_format["questions"]):
        question_text = question_data["question"]
        options = [
            question_data["optionA"],
            question_data["optionB"],
            question_data["optionC"],
            question_data["optionD"],
        ]
        correct_option = question_data["correctOption"]

        try:
            context.bot.send_chat_action(
                chat_id=update.effective_chat.id, action=ChatAction.TYPING
            )
            sent_poll = context.bot.send_poll(
                chat_id=update.effective_chat.id,
                question=question_text,
                options=options,
                type=Poll.QUIZ,
                correct_option_id=ord(correct_option[-1]) - ord("A"),
                is_anonymous=False,
                explanation=f'Correct Answer: {question_data["explanation"]}',
                open_period=20,
            )
            polls_sent_count += 1
            poll_ids.append(sent_poll.poll.id)
            poll_message_id.append(sent_poll.message_id)
            user_answers[sent_poll.poll.id] = correct_option
        except:
            logging.info(i)
            try:
                context.bot.send_chat_action(
                    chat_id=update.effective_chat.id, action=ChatAction.TYPING
                )
                sent_poll = context.bot.send_poll(
                    chat_id=update.effective_chat.id,
                    question=question_text,
                    options=options,
                    type=Poll.QUIZ,
                    correct_option_id=ord(correct_option[-1]) - ord("A"),
                    is_anonymous=False,
                    explanation="Explanation will be sent when the quiz ends",
                    open_period=20,
                )
                polls_sent_count += 1
                poll_ids.append(sent_poll.poll.id)
                poll_message_id.append(sent_poll.message_id)
                user_answers[sent_poll.poll.id] = correct_option
            except:
                pass
    logging.info("done")
    time.sleep(20)
    send_explanation(update=update, context=context)


# dispatcher
def register(dispatcher):
    try:
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("result", send_rankings))
        conv_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.document, Enterfile)],
            states={
                START_PAGE: [
                    MessageHandler(Filters.text & ~Filters.command, set_start)
                ],
                END_PAGE: [MessageHandler(Filters.text & ~Filters.command, set_end)],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
        )
        dispatcher.add_handler(conv_handler)
        dispatcher.add_handler(CallbackQueryHandler(button_callback))
        dispatcher.add_handler(PollAnswerHandler(poll_answer_handler))
        dispatcher.add_handler(CommandHandler("help", help))
    except:
        pass


# driver function
def main():
    updater = Updater(token=TOKEN)
    register(updater.dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
