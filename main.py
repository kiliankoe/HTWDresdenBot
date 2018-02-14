import os
from telegram.ext import Updater
from htwdresden_bot import *


def on_startup(bot, _):
    maintainer_chat_id = os.getenv('MAINTAINER_CHAT_ID')
    if maintainer_chat_id is not None:
        bot.send_message(chat_id=maintainer_chat_id, text='Running...')


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

updater.start_polling()
