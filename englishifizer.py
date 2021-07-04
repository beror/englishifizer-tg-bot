# Quick way: allow for one transliterated word in a relatively long period [CURRENT IMPLEMENTATION]
# Proper way: look for the surroundings of the questionable word
#   (enough English words surround the word -> let it pass)


from telegram import *
from telegram.ext import *
from langdetect import lang_detect_exception

import datetime
from sys import exc_info

from language_processing import *
from database import *

targets_username = "" # without the "@" # EDIT ME

init_db()


def start(update: Update, context: CallbackContext) -> None:
    print("\n@" + update.message.from_user.username + " started me")
    print_message_info(update, context)
    print("------------------------------")

    # context.bot.send_message(update.message.chat.id, "Hello") # message to respond to the "/start" command # EDIT ME

    # if update.message.from_user.username == targets_username:
    #     update.message.reply_text(text="Hey, my dear target") # reply message text that is sent if "/start" was sent by target # EDIT ME
    #     context.bot.send_message(update.message.chat.id, "Have fun!") # message text that is sent if "/start" was sent by target # EDIT ME

def process_targets_message(update: Update, context: CallbackContext) -> None:
    time_unix = int(datetime.datetime.now().timestamp())

    messageText = update.message.text

    print('\n')
    print_message_info(update, context)

    if messageText == None:
        print("------------------------------") # TODO: get rid of this duplication of printing dashes at the end of the function
        return

    spelling_mistakes_count = get_spelling_mistakes_count(messageText)
    langs_detected = None

    try:
        langs_detected = detect_langs(messageText)
    except lang_detect_exception.LangDetectException:
        print("Couldn't detect language")

        execute_targets_messages_table_query(str(update.message), is_correct=None, is_allowed=True, spelling_mistakes_count=spelling_mistakes_count, lang_probabilities=None, time_unix=time_unix)

    for lang_detected in langs_detected:
        if lang_detected.lang == "ru" or lang_detected.lang == "uk" or lang_detected.lang == "bg" or lang_detected.lang == "mk":
            print("langdetect: Slavic")

            context.bot.delete_message(update.message.chat.id, update.message.message_id)

            execute_targets_messages_table_query(str(update.message), is_correct=False, is_allowed=False, spelling_mistakes_count=spelling_mistakes_count, lang_probabilities=str(langs_detected), time_unix=time_unix)
    if len(messageText.split()) < 6:
        if spelling_mistakes_count > 0:
            if(last_incorrect_targets_message_was_not_so_long_ago()):
                print("Spelling mistakes count > 0 & last incorrect message was not so long ago")

                context.bot.delete_message(update.message.chat.id, update.message.message_id)

                execute_targets_messages_table_query(str(update.message), is_correct=False, is_allowed=False, spelling_mistakes_count=spelling_mistakes_count, lang_probabilities=None, time_unix=time_unix)
            else:
                print("Spelling mistakes count > 0 & last incorrect message was long time ago")

                execute_targets_messages_table_query(str(update.message), is_correct=False, is_allowed=True, spelling_mistakes_count=spelling_mistakes_count, lang_probabilities=None, time_unix=time_unix)
        else:
            print("Spelling mistakes count is not > 0")

            execute_targets_messages_table_query(str(update.message), is_correct=True, is_allowed=True, spelling_mistakes_count=spelling_mistakes_count, lang_probabilities=None, time_unix=time_unix)
    else:
        if langs_detected[0].lang == "en":
            print("langdetect: English")

            execute_targets_messages_table_query(str(update.message), is_correct=True, is_allowed=True, spelling_mistakes_count=spelling_mistakes_count, lang_probabilities=str(langs_detected), time_unix=time_unix)
        else:
            print("langdetect: Not English")

            execute_targets_messages_table_query(str(update.message), is_correct=False, is_allowed=False, spelling_mistakes_count=spelling_mistakes_count, lang_probabilities=str(langs_detected), time_unix=time_unix)

            context.bot.delete_message(update.message.chat.id, update.message.message_id)

    print("------------------------------")

def print_message_info(update: Update, context: CallbackContext) -> None:
    print("Message information:")
    print(update.message, '\n')


BOT_TOKEN = "" # EDIT ME
updater = Updater(BOT_TOKEN)

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(MessageHandler(Filters.user(username=targets_username), process_targets_message))

PORT = os.environ.get("PORT", 5000)

updater.start_webhook( # webhook info. You probably need to edit only the "webhook_url" argument. It's possible to change this to argumentless ".start_polling()" and the bot will work and webhooks are superior
    listen="0.0.0.0",
    port=PORT,
    url_path=BOT_TOKEN,
    webhook_url="https://englishifizer.herokuapp.com/" + BOT_TOKEN)

updater.idle()