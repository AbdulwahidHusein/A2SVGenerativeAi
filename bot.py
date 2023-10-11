import logging
import os
import openai
import sys

from quiz_app import generator

sys.path.append("..")
from telegram import (
    Message,
    ChatAction,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    File,
)
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    Updater,
    CallbackQueryHandler,
)
import requests
from dotenv import load_dotenv
import json


load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")
TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

user_data = {}
question_format = {}
file = None
START_PAGE = 0
END_PAGE = 1
difficulty = "not difficult"


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter file")


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello There, please enter file so we can change it to qize for you!"
    )


def set_difficulty(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Easy", callback_data="easy")],
        [InlineKeyboardButton("Medium", callback_data="medium")],
        [InlineKeyboardButton("Difficult", callback_data="difficult")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Choose Difficulty:", reply_markup=reply_markup)


def set_end(update: Update, context: CallbackContext):
    end = update.message.text
    user_data["end_page"] = int(end)
    update.message.reply_text(
        f"Start page: {user_data['start_page']}\nEnd page: {user_data['end_page']}"
    )
    set_difficulty(update=update, context=context)


def set_start(update: Update, context: CommandHandler):
    start = update.message.text
    user_data["start_page"] = int(start)
    update.message.reply_text("Enter end page")
    return END_PAGE


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END


def Enterfile(update: Update, context: CallbackContext):
    global user_data
    global file
    file = update.message.document
    file_recieved = context.bot.get_file(file_id=file.file_id)
    file_name = file.file_name
    # file_path = file_recieved.file_path
    user_data["file_name"] = file_name
    file_downloaded = file_recieved.download()
    user_data["file"] = file_downloaded
    with open(file_downloaded, "rb") as f:
        user_data["file"] = file_downloaded

    reply_text = f"Recieved file: {user_data['file_name']}"
    user_data["file_name"] = file_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_text + "\nEnter start page:"
    )
    return START_PAGE


def button_callback(update: Update, context: CallbackContext):
    global user_data
    global difficulty
    query = update.callback_query
    if query.data.isalnum():
        user_data["difficulty"] = query.data
        query.message.reply_text(
            f"diffiiculty set to {user_data['difficulty']}",
        )
        send_request(update=update, context=context)


def send_request(update: Update, context: CallbackContext):
    global user_data
    global question_format
    with open(user_data["file"], "rb") as f:
        question_format = generator.get_question(
            f,
            5,
            user_data["difficulty"],
            int(user_data["start_page"]),
            int(user_data["end_page"]),
            mode="multiple_choice",
            model="chatgpt",
        )

    logging.info("request sent")
    print(question_format)
    context.bot.send_message(chat_id=update.effective_chat.id, text=question_format)


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.document, Enterfile)],
        states={
            START_PAGE: [MessageHandler(Filters.text & ~Filters.command, set_start)],
            END_PAGE: [MessageHandler(Filters.text & ~Filters.command, set_end)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.add_handler(CommandHandler("help", help))


def main():
    updater = Updater(token=TOKEN)
    register(updater.dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    # with open("his.pdf", "rb") as f:
    #     for line in f:
    #         print(line)
    #     # question = generator.get_question(
    #     #     f, 5, "easy", 2, 3, "multiple_choice", "chat_gpt"
    #     # )
    #     # print(question)
    main()
