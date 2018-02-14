import sys
import time
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
                                  'Zukunft direkt via /noten abrufen und ich rufe deine Noten regelmäßig automatisch '
                                  'für dich ab und benachrichtige dich bei Änderungen.')
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

    if grades is not None:
        grades_msg = '\n'.join([str(g) for g in grades])
    else:
        grades_msg = None

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


def _fetch_grades(login: RZLogin) -> [Grade] or None:
    try:
        course = Course.fetch(login)[0]  # can this contain multiple courses?
        grades = Grade.fetch(login, course.degree_nr, course.course_nr, course.reg_version)
        grades = sorted(grades, key=lambda grade: grade.exam_date if grade.exam_date is not None else '0000')
    except Exception as e:
        print(f'Failed fetching grades for {login} with {e}', file=sys.stderr)
        return None
    return grades


def notify_grades(bot, job):
    """Fetch grades of all logged in users and send them notifications if new grades are available."""
    all_users = db.fetch_all_logins()
    for user in all_users:
        chat_id = user[0]
        grade_count = user[1]
        login = user[2]

        current_grades = _fetch_grades(login)
        if current_grades is None:
            # grades API seems to be offline a lot, stop the entire update in that case
            break

        if grade_count == -1:
            # grades have never been fetched for this user, not sending a notification at this time
            db.update_grade_count_for_user(login.s_number, len(current_grades))
            time.sleep(2)
            continue

        if len(current_grades) == grade_count:
            time.sleep(2)
            continue

        grade_diff = len(current_grades) - grade_count
        db.update_grade_count_for_user(login.s_number, len(current_grades))
        bot.send_message(chat_id=chat_id, text='{} neue Noten verfügbar! /noten?'.format(grade_diff))

        time.sleep(2)  # just in case, don't want to stress the endpoint too much
