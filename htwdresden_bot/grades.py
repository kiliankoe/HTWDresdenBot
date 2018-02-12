from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from htwdresden import RZLogin, Course, Grade
from htwdresden_bot import db


def _grades_cmd(bot, update, args):
    if len(args) is 2:
        login = RZLogin(args[0], args[1])
    else:
        login = db.fetch_login_for_user(update.message.chat.username)

    if login is None:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Um deine Noten abzurufen benötige ich deinen RZLogin (sNummer und Passwort).\n'
                              'Um den Login zu speichern nutze bitte den `/login` Befehl.\n\nAlternativ kannst du '
                              'auch deine sNummer und dein Passwort an diesen Befehl anhängen, dann wird dein Login '
                              'nicht persistiert und nur dieses eine Mal genutzt um deine Noten abzurufen.')
        return
    grades_msg = _fetch_grades(login)
    bot.send_message(chat_id=update.message.chat_id,
                     text='```\n{}\n```'.format(grades_msg),
                     parse_mode=ParseMode.MARKDOWN)


grades_handler = CommandHandler('noten', _grades_cmd, pass_args=True)


def _fetch_grades(login: RZLogin) -> str:
    course = Course.fetch(login)[0]  # can this contain multiple courses?
    grades = Grade.fetch(login, course.degree_nr, course.course_nr, course.reg_version)#.sort(key=lambda grade: grade.exam_date)
    return _format_grades(grades)


def _format_grades(grades: [Grade]) -> str:
    formatted_grades = [str(g) for g in grades]
    return '\n'.join(formatted_grades)
