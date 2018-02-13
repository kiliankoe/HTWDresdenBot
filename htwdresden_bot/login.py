import sys
from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from htwdresden import RZLogin, Course, HTWAuthenticationException
from htwdresden_bot import db


def _login_cmd(_, update, args):
    if len(args) != 2:
        update.message.reply_text('Hierfür benötige ich deine sNummer und dein Passwort. Benutze bitte die Syntax\n'
                                  '`/login s12345 dein_passwort`',
                                  parse_mode=ParseMode.MARKDOWN)
        return

    login = RZLogin(args[0], args[1])

    try:
        Course.fetch(login)
    except HTWAuthenticationException:
        update.message.reply_text('Dieser Login scheint nicht zu funktionieren. Sicher, dass die Daten so korrekt '
                                  'sind?')
        return
    except:
        pass

    ok = db.persist_login(update.message.chat_id, login)
    if ok:
        update.message.reply_text('Dein Login wurde gespeichert ✔')
    else:
        update.message.reply_text('Dein Login konnte leider nicht gespeichert werden. Kenne ich ihn vielleicht schon?'
                                  '\n\nWenn du dein Passwort ändern willst, dann sende bitte /logout um den alten '
                                  'Login zu löschen. Sorry für die Umstände.')


login_handler = CommandHandler('login', _login_cmd, pass_args=True)


def _logout_cmd(_, update):
    ok = db.remove_login(update.message.chat_id)
    if ok:
        update.message.reply_text('Dein gespeicherter Login wurde erfolgreich gelöscht ✔')
    else:
        update.message.reply_text('Dein Login konnte nicht gelöscht werden. Kannte ich ihn überhaupt? 🤔')


logout_handler = CommandHandler('logout', _logout_cmd)
