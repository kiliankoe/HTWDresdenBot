from telegram.ext import CommandHandler


def _start_cmd(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Hallo, ich bin der HTW Bot. Tippe `/` um Vorschläge für meine möglichen Aktionen zu sehen.')


start_handler = CommandHandler('start', _start_cmd)
