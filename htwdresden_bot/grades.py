import sys
from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from htwdresden import RZLogin, Course, Grade, HTWAuthenticationException
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

    if grades_msg == '':
        bot.send_message(chat_id=update.message.chat_id,
                         text='Konnte keine Noten finden. 🤔')
    elif grades_msg is None:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Fehler beim Abrufen deiner Noten. 👀\n\nEin /logout und anschließender /login hilft '
                              'bestimmt. 🤞')
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text='```\n{}\n```'.format(grades_msg),
                         parse_mode=ParseMode.MARKDOWN)


grades_handler = CommandHandler('noten', _grades_cmd, pass_args=True)


def _fetch_grades(login: RZLogin) -> str:
    try:
        course = Course.fetch(login)[0]  # can this contain multiple courses?
        grades = Grade.fetch(login, course.degree_nr, course.course_nr, course.reg_version)#.sort(key=lambda grade: grade.exam_date)
    except HTWAuthenticationException:
        print(f'Failed auth on fetching grades for {login}', file=sys.stderr)
        return None
    return _format_grades(grades)


def _format_grades(grades: [Grade]) -> str:
    formatted_grades = [str(g) for g in grades]
    return '\n'.join(formatted_grades)
