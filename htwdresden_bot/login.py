from telegram.ext import CommandHandler
from htwdresden_bot import db


def _login_cmd(bot, update, args):
    if len(args) != 2:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Hierfür benötige ich deine sNummer und dein Passwort. Benutze bitte die Syntax '
                              '`/login s12345 dein_passwort`.')
        return
    ok = db.persist_login(update.message.chat.username, args[0], args[1])
    if ok:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Dein Login wurde gespeichert ✔')
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Dein Login konnte leider nicht gespeichert werden. Kenne ich ihn vielleicht schon?')


login_handler = CommandHandler('login', _login_cmd, pass_args=True)


# def _change_password_cmd(bot, update, args):
#     raise NotImplementedError  # TODO
#     pass
#
#
# change_password_handler = CommandHandler('pw_aendern', _change_password_cmd, pass_args=True)


def _logout_cmd(bot, update):
    ok = db.remove_login(update.message.chat.username)
    if ok:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Deine gespeicherten Login Daten wurden erfolgreich gelöscht ✔')
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Dein Login konnte nicht gelöscht wurden. Kannte ich ihn überhaupt? 🤔')


logout_handler = CommandHandler('logout', _logout_cmd)
