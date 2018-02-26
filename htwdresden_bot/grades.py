import sys
import time
import logging

from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from telegram.chataction import ChatAction
from htwdresden import RZLogin, Course, Grade
from htwdresden.exceptions import *
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

    try:
        grades = _fetch_grades(login)
        grades_msg = _format_grades(grades)
        average = calculate_grade_average(grades)
        average_msg = 'Notendurchschnitt {0:.2f}'.format(average)
    except HTWBaseException:
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
        update.message.reply_text('```\n{}\n\n{}\n```\n\nAlle Angaben ohne Gewähr. Eine detaillierte Auflistung findest du '
                                  '[hier](https://wwwqis.htw-dresden.de).'.format(grades_msg, average_msg),
                                  parse_mode=ParseMode.MARKDOWN)


grades_handler = CommandHandler('noten', _grades_cmd, pass_args=True)


def _fetch_grades(login: RZLogin) -> [Grade] or None:
    course = Course.fetch(login)[0]  # TODO: support all courses, not just the first one
    grades = Grade.fetch(login, course.degree_nr, course.course_nr, course.reg_version)
    grades = sorted(grades, key=lambda grade: grade.semester)
    return grades


def _format_grades(grades: [Grade]) -> str:
    if len(grades) == 0:
        return ''

    output = []
    current_semester = grades[0].semester
    output.append(_format_semester(current_semester))

    for grade in grades:
        if grade.semester == current_semester:
            output.append(str(grade))
        else:
            current_semester = grade.semester
            output.append('\n')
            output.append(_format_semester(current_semester))
            output.append(str(grade))

    return '\n'.join(output)

def calculate_grade_average(grades: [Grade]) -> float:
    if len(grades) == 0:
        return 0.0

    sumWeightedGrades = 0.0
    sumCredits = 0.0

    for grade in grades:
        sumWeightedGrades += grade.ects_credits * grade.grade
        sumCredits += grade.ects_credits

    if sumCredits == 0.0:
        return 0.0

    return sumWeightedGrades / sumCredits

def _format_semester(semester: int) -> str:
    semester = str(semester)
    ident = semester[-1]
    year = semester[:4]

    if ident == '1':
        return 'Sommersemester {}'.format(year)
    else:
        return 'Wintersemester {}'.format(year)


def notify_grades(bot, _):
    """Fetch grades of all logged in users and send them notifications if new grades are available."""
    all_users = db.fetch_all_logins()
    for user in all_users:
        logging.debug(f'updating grades for {user[0]}')
        chat_id = user[0]
        grade_count = user[1]
        login = user[2]

        try:
            current_grades = _fetch_grades(login)
        except HTWAuthenticationException:
            db.remove_login(chat_id)
            bot.send_message(chat_id=chat_id,
                             text='Der Server der HTW meint dein Login sei nicht (mehr) valide. Ich habe diesen aus '
                                  'meiner Datenbank entfernt und werde *nicht* mehr für dich nach neuen Noten schauen. '
                                  'Solltest du nur dein Passwort geändert haben, so sende mir bitte erneut den '
                                  '/login Befehl mit deinen Logindetails.',
                             parse_mode=ParseMode.MARKDOWN)
            continue
        except HTWServerException as e:
            # stop the entire update if the server is down
            logging.error(f'grades api error {e}')
            return

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

        if grade_diff < 0:
            bot.send_message(chat_id=chat_id, text='{} Noten wurden entfernt! /noten?'.format(-grade_diff))
        elif grade_diff == 1:
            bot.send_message(chat_id=chat_id, text='Eine neue Note ist verfügbar! /noten?'.format(grade_diff))
        else:
            bot.send_message(chat_id=chat_id, text='{} neue Noten sind verfügbar! /noten?'.format(grade_diff))

        time.sleep(2)  # just in case, don't want to stress the endpoint too much
