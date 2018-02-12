import sys
from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from htwdresden import RZLogin, Course, Grade, HTWAuthenticationException
from htwdresden_bot import db


def _grades_cmd(_, update, args):
    if len(args) is 2:
        login = RZLogin(args[0], args[1])
    else:
        login = db.fetch_login_for_user(update.message.chat_id)

    if login is None:
        update.message.reply_text('Um deine Noten abzurufen benötige ich deinen RZLogin (sNummer und Passwort).\nUm '
                                  'den Login zu speichern nutze bitte den `/login` Befehl.\n\nAlternativ kannst du '
                                  'auch deine sNummer und dein Passwort an diesen Befehl anhängen, dann wird dein '
                                  'Login nicht persistiert und nur dieses eine Mal genutzt um deine Noten abzurufen.')
        return
    grades_msg = _fetch_grades(login)

    if grades_msg == '':
        update.message.reply_text('Konnte keine Noten finden. 🤔')
    elif grades_msg is None:
        update.message.reply_text('Fehler beim Abrufen deiner Noten. 👀\n\nEin /logout und anschließender /login hilft '
                                  'bestimmt. 🤞')
    else:
        update.message.reply_text('```\n{}\n```'.format(grades_msg),
                                  parse_mode=ParseMode.MARKDOWN)


grades_handler = CommandHandler('noten', _grades_cmd, pass_args=True)


def _fetch_grades(login: RZLogin) -> str:
    try:
        course = Course.fetch(login)[0]  # can this contain multiple courses?
        grades = Grade.fetch(login, course.degree_nr, course.course_nr, course.reg_version)
        grades = sorted(grades, key=lambda grade: grade.exam_date if grade.exam_date is not None else '0000')
    except HTWAuthenticationException:
        print(f'Failed auth on fetching grades for {login}', file=sys.stderr)
        return None
    return '\n'.join([str(g) for g in grades])
