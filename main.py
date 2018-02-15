import os
from telegram.ext import Updater
from telegram.error import TelegramError, Unauthorized
from htwdresden_bot import *


GRADE_NOTIFICATION_INTERVAL = 3_600


def on_startup(bot, _):
    maintainer_chat_id = os.getenv('MAINTAINER_CHAT_ID')
    if maintainer_chat_id is not None:
        bot.send_message(chat_id=maintainer_chat_id, text='Running...')


def error_handler(bot, update, error):
    try:
        raise error
    except Unauthorized:
        # user has blocked this bot, no need to update grades anymore
        db.remove_login(update.message.chat_id)
    except TelegramError:
        pass


db.setup()

updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'))
updater.job_queue.run_once(on_startup, 0)

dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(login_handler)
dispatcher.add_handler(logout_handler)
dispatcher.add_handler(grades_handler)
dispatcher.add_handler(free_rooms_handler)
dispatcher.add_handler(meals_handler)
dispatcher.add_handler(meal_search_handler)

dispatcher.add_error_handler(error_handler)

updater.job_queue.run_repeating(notify_grades, interval=GRADE_NOTIFICATION_INTERVAL, first=0)

updater.start_polling()
