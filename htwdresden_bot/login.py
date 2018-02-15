import logging

from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from htwdresden import RZLogin, Course, HTWAuthenticationException
from htwdresden_bot import db


def _login_cmd(_, update, args):
    if len(args) == 1 and args[0].lower() == 'hilfe':
        update.message.reply_text('Hinterlege bei mir deine S-Nummer und dein Passwort, damit ich regelmäßig für dich '
                                  'nach neuen Noten schauen kann. Wenn ich Änderungen feststellen kann, schicke ich '
                                  'dir eine Benachrichtigung. Ebenso kannst du nach dem Login den /noten Befehl ohne '
                                  'Angabe deiner Details nutzen.')
        return

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
        logging.info('failed login auth, not persisting login details')
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
        logging.warning('failed to persist login')


login_handler = CommandHandler('login', _login_cmd, pass_args=True)


def _logout_cmd(_, update, args):
    if len(args) == 1 and args[0].lower() == 'hilfe':
        update.message.reply_text('Mit /logout kannst du deinen bei mir hinterlegten Login löschen. Ich kann dir dann '
                                  'selbstverständlich auch keine Benachrichtigungen bei neuen Noten mehr schicken.')
        return

    ok = db.remove_login(update.message.chat_id)
    if ok:
        update.message.reply_text('Dein gespeicherter Login wurde erfolgreich gelöscht ✔')
    else:
        update.message.reply_text('Dein Login konnte nicht gelöscht werden. Kannte ich ihn überhaupt? 🤔')
        logging.warning('failed to remove login')


logout_handler = CommandHandler('logout', _logout_cmd, pass_args=True)
