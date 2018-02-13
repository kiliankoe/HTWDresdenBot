import sys
from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from telegram.chataction import ChatAction
from htwdresden import RZLogin, Course, Grade
from htwdresden_bot import db


def _grades_cmd(bot, update, args):

    if len(args) == 1 and args[0].lower() == 'hilfe':
        update.message.reply_text('Mit /noten kannst du deine Noten abrufen. Hierfür ist natürlich dein RZLogin '
                                  'erforderlich. Den kannst du mir entweder via /login permanent (zumindest bis du '
                                  'dich via /logout wieder bei mir abmeldest) überlassen oder mit '
                                  '\'/noten s12345 dein_password\' nur einmal übergeben, wobei dieser dann nicht '
                                  'gespeichert wird. Solltest du deinen Login hinterlegen kannst du deine Noten in '
                                  'Zukunft direkt via /noten abrufen.')
        return

    if len(args) == 2:
        login = RZLogin(args[0], args[1])
    else:
        login = db.fetch_login_for_user(update.message.chat_id)

    if login is None:
        update.message.reply_text('Um deine Noten abzurufen benötige ich deinen RZLogin (sNummer und Passwort).\nUm '
                                  'den Login zu speichern nutze bitte den /login Befehl.\n\nAlternativ kannst du auch '
                                  'deine sNummer und dein Passwort an diesen Befehl anhängen, dann wird dein Login '
                                  'nicht persistiert und nur dieses eine Mal genutzt um deine Noten abzurufen.')
        return

    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    grades = _fetch_grades(login)
    grades_msg = '\n'.join([str(g) for g in grades])

    if grades_msg == '':
        update.message.reply_text('Konnte keine Noten finden. 🤔')
    elif grades_msg is None:
        update.message.reply_text('Fehler beim Abrufen deiner Noten. 👀\n\nEin /logout und anschließender /login hilft '
                                  'bestimmt. 🤞\nAlternativ kannst du auch direkt beim '
                                  '[QIS Portal](https://wwwqis.htw-dresden.de) vorbeischauen, hoffentlich klappt ja '
                                  'zumindest das. 😅',
                                  parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text('```\n{}\n```\n\nAlle Angaben ohne Gewähr. Eine detaillierte Auflistung findest du '
                                  '[hier](https://wwwqis.htw-dresden.de).'.format(grades_msg),
                                  parse_mode=ParseMode.MARKDOWN)


grades_handler = CommandHandler('noten', _grades_cmd, pass_args=True)


def _fetch_grades(login: RZLogin) -> [Grade]:
    try:
        course = Course.fetch(login)[0]  # can this contain multiple courses?
        grades = Grade.fetch(login, course.degree_nr, course.course_nr, course.reg_version)
        grades = sorted(grades, key=lambda grade: grade.exam_date if grade.exam_date is not None else '0000')
    except Exception as e:
        print(f'Failed fetching grades for {login} with {e}', file=sys.stderr)
        return []
    return grades
