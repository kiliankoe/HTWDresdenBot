from telegram.ext import CommandHandler
from htwdresden import RZLogin, Course, Grade


def _grades_cmd(bot, update, user_data):
    if 'rzlogin' not in user_data:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Um deine Noten abzurufen benötige ich deinen RZLogin (sNummer und Passwort). '
                              'Dieser wird selbstverständlich nur kurzlebig gespeichert.\nUm den Login zu speichern '
                              'nutze bitte den `/login` Befehl.\n\nSolltest du deinen Login bereits einmal eingegeben '
                              'haben dann wurde ich wohl zwischenzeitlich neu gestartet und habe ihn vergessen. '
                              'Sorry 😅')
        return
    login = RZLogin(user_data.get('rzlogin')[0], user_data.get('rzlogin')[1])
    grades_msg = _fetch_grades(login)
    bot.send_message(chat_id=update.message.chat_id, text=grades_msg)


grades_handler = CommandHandler('noten', _grades_cmd, pass_user_data=True)


def _fetch_grades(login: RZLogin) -> str:
    course = Course.fetch(login)[0]  # can this contain multiple courses?
    grades = Grade.fetch(login, course.degree_nr, course.course_nr, course.reg_version)#.sort(key=lambda grade: grade.exam_date)
    return _format_grades(grades)


def _format_grades(grades: [Grade]) -> str:
    formatted_grades = []
    for g in grades:
        date = g.exam_date if g.exam_date is not None else 'n/a'
        title = g.title
        grade = int(g.grade) / 100 if g.grade is not None else 'n/a'

        formatted_grades.append('{} {} {}'.format(date, title, grade))

    return '\n'.join(formatted_grades)
