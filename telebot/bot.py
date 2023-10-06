import logging
import os
import openai
from telegram import (
    Message,
    ChatAction,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
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
from telegram import Bot
import file_handler
from dotenv import load_dotenv
import json

load_dotenv()
question_format = {
    "JS": [
        {
            "id": 1,
            "question": "Question number 1",
            "options": ["option a", "option b", "option c", "option d"],
            "answer": "option c",
            "score": 0,
            "status": "",
            "user_answer": "",
            "explanation": "brief explanation",
        },
        {
            "id": 2,
            "question": "Question number 2",
            "options": ["option a", "option b", "option c", "option d"],
            "answer": "option c",
            "score": 0,
            "status": "",
            "user_answer": "",
            "explanation": "brief explanation",
        },
    ]
}

openai.api_key = os.environ.get("OPENAI_API_KEY")


TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

user_data = {}
start_flag = 0
difficulty = "not difficult"


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter file")


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello There, please enter file so we can change it to qize for you!"
    )


def create_buttons(num_pages):
    buttons = []

    for page_num in range(1, num_pages + 1):
        button = InlineKeyboardButton(str(page_num), callback_data=str(page_num))

        buttons.append(button)

    return buttons


def create_keyboard_markup(buttons, buttons_per_row=2):
    keyboard = []
    row = []
    for i, button in enumerate(buttons, start=1):
        row.append(button)
        if i % buttons_per_row == 0 or i == len(buttons):
            keyboard.append(row)
            row = []
    return InlineKeyboardMarkup(keyboard)


def Enterfile(update: Update, context: CallbackContext):
    file = update.message.document
    file_recieved = context.bot.get_file(file_id=file.file_id)
    file_name = file.file_name
    file_size = file.file_size

    file_recieved.download(file_name)
    update.message.reply_text("Successs")

    reply_text = f"Recieved file: {file_name}\nFile size : {file_size} \n\nPlease choose the start page:"

    global user_data
    try:
        user_data["file_name"] = file_name
    except:
        user_data.setdefault("file_name", file_name)

    text = file_handler.FileHandler(file_name)
    number_pages = text.page_num(file_name)
    buttons = create_buttons(num_pages=number_pages)
    keyboard_markup = create_keyboard_markup(buttons=buttons)
    update.message.reply_text(reply_text, reply_markup=keyboard_markup)


def set_difficulty(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Easy", callback_data="easy")],
        [InlineKeyboardButton("Medium", callback_data="medium")],
        [InlineKeyboardButton("Difficult", callback_data="difficult")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def show_difficulty(update: Update, context: CallbackContext):
    keyboard_markup = set_difficulty(update=update, context=context)
    reply_text = "choose difficulty:"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_text, reply_markup=keyboard_markup
    )


def button_callback(update: Update, context: CallbackContext):
    global user_data
    global start_flag
    global difficulty
    query = update.callback_query
    try:
        page_number = int(query.data)
    except:
        command = query.data
    if query.data.isdigit() and start_flag == 0:
        try:
            user_data["start_page_text"] = page_number
        except:
            user_data.setdefault("start_page_text", page_number)
        start_flag = 1
        query.message.reply_text(
            text=f"start page set to {user_data['start_page_text']}",
        )
        logging.info("start page set")
    elif query.data.isdigit() and start_flag == 1:
        try:
            user_data["end_page_text"] = page_number
        except:
            user_data.setdefault("end_page_text", page_number)
        query.message.reply_text(
            f"End page set to {user_data['end_page_text']}",
        )
        logging.info("end page set")
        start_flag = 0
        show_difficulty(update=update, context=context)
    else:
        difficulty = query.data
        user_data["difficulty"] = difficulty
        send_request(update=update, context=context)


def send_request(update: Update, context: CallbackContext):
    text = file_handler.FileHandler(user_data["file_name"])
    start_page = int(user_data["start_page_text"])
    end_page = int(user_data["end_page_text"])
    text.read_file(spage=start_page, epage=end_page)
    processed_string = text.summerized()
    number_of_questions = 5
    user_message = f"""generate a quiz contining {number_of_questions} different multiple choice questions with 
    different context containing four choices with {user_data['difficulty']} difficulty the questions must be returned in 
    the following format {question_format} note the 
    question must be in json format!!! also make sure the explanations must be less than 2 lines important!.
    NOTE only use the following text for the generation of quiz {processed_string}"""
    print(user_data["difficulty"])
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_message,
        max_tokens=2000,
        temperature=0.1,
        n=1,
        stop=None,
    )
    bot_response = response.choices[0].text.strip()
    json_start_index = bot_response.find("{'JS':")
    json_text = bot_response[json_start_index:]

    context.bot.send_message(chat_id=update.effective_chat.id, text=json_text)


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document & ~Filters.text, Enterfile))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.add_handler(CommandHandler("help", help))


def main():
    updater = Updater(token=TOKEN)
    register(updater.dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
