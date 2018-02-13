import os
from telegram.ext import Updater
from htwdresden_bot import *

db.setup()

updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(version_handler)
dispatcher.add_handler(login_handler)
dispatcher.add_handler(logout_handler)
dispatcher.add_handler(grades_handler)
dispatcher.add_handler(free_rooms_handler)
dispatcher.add_handler(meals_handler)
dispatcher.add_handler(meal_search_handler)

updater.start_polling()
