import os
from telegram.ext import Updater

from htwdresden_bot import *

updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(login_handler)
dispatcher.add_handler(logout_handler)
dispatcher.add_handler(grades_handler)

updater.start_polling()
