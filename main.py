import os
import logging
import argparse
from telegram.ext import Updater
from telegram.error import TelegramError, Unauthorized
from htwdresden_bot import *

parser = argparse.ArgumentParser()
parser.add_argument('--log', dest='loglevel', default='ERROR', help='log level')
args = parser.parse_args()

numeric_level = getattr(logging, args.loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: {}'.format(args.loglevel))
logging.basicConfig(level=numeric_level)


GRADE_NOTIFICATION_INTERVAL = 3_600

db.setup()

updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'))

dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(login_handler)
dispatcher.add_handler(logout_handler)
dispatcher.add_handler(grades_handler)
dispatcher.add_handler(free_rooms_handler)
dispatcher.add_handler(meals_handler)
dispatcher.add_handler(meal_search_handler)

logging.info('Polling for new messages...')
updater.start_polling()

updater.job_queue.run_repeating(notify_grades, interval=GRADE_NOTIFICATION_INTERVAL, first=0)


def error_handler(bot, update, error):
    try:
        raise error
    except Unauthorized:
        # user has blocked this bot, no need to update grades anymore
        db.remove_login(update.message.chat_id)
    except TelegramError as e:
        logging.error(f'unexpected telegram error {e}')
        pass


dispatcher.add_error_handler(error_handler)
