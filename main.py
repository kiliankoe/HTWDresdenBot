import os

from htwdresden import RZLogin, Course, Grade
from telegram.ext import CommandHandler
from telegram.ext import Updater


updater = Updater(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hallo, ich bin der HTW Bot. Du kannst mich u.a. nach deinen aktuellen Noten fragen.')

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def grades(bot, update, args):
    if len(args) != 2:
        bot.send_message(chat_id=update.message.chat_id, text='Um deine Noten zu laden benötige ich deine sNummer und dein Passwort. Benutze bitte die Syntax `/noten s12345 dein_passwort`.')
        return
    login = RZLogin(args[0], args[1])
    main_course = Course.fetch(login)[0]
    grades = Grade.fetch(login, main_course.degree_nr, main_course.course_nr, main_course.reg_version)
    grades_str = '\n'.join([f'{grade.title} {grade.grade}' for grade in grades])
    bot.send_message(chat_id=update.message.chat_id, text=f'{len(grades)} Noten gefunden.\n\n{grades_str}')

grades_handler = CommandHandler('noten', grades, pass_args=True)
dispatcher.add_handler(grades_handler)

updater.start_polling()
