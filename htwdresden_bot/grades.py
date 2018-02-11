from telegram.ext import CommandHandler
from htwdresden import RZLogin, Course, Grade


def _grades_cmd(bot, update, user_data):
    if 'rzlogin' not in user_data:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Um deine Noten abzurufen benötige ich leider deinen RZLogin (sNummer und Passwort). ' +
                              'Dieser wird selbstverständlich nur kurzlebig gespeichert.\nUm den Login zu speichern ' +
                              'nutze bitte den `/login` Befehl.')
        return
    login = RZLogin(user_data.get('rzlogin')[0], user_data.get('rzlogin')[1])
    main_course = Course.fetch(login)[0]
    grades = Grade.fetch(login, main_course.degree_nr, main_course.course_nr, main_course.reg_version)
    grades_str = '\n'.join([f'{grade.title} {grade.grade}' for grade in grades])
    bot.send_message(chat_id=update.message.chat_id, text=f'{len(grades)} Noten gefunden.\n\n{grades_str}')


grades_handler = CommandHandler('noten', _grades_cmd, pass_user_data=True)
