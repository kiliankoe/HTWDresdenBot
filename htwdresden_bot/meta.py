from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode


def _start_cmd(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=f'Hi {update.message.chat.first_name} 👋,\ntippe `/` um Vorschläge für meine möglichen '
                          f'Aktionen zu sehen.',
                     parse_mode=ParseMode.MARKDOWN)


start_handler = CommandHandler('start', _start_cmd)
