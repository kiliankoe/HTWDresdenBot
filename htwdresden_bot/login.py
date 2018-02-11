from telegram.ext import CommandHandler


def _login_cmd(bot, update, args, user_data):
    if len(args) != 2:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Hierfür benötige ich deine sNummer und dein Passwort. Benutze bitte die Syntax '
                              '`/login s12345 dein_passwort`.')
        return
    user_data['rzlogin'] = args
    bot.send_message(chat_id=update.message.chat_id,
                     text='Dein Login wurde gespeichert ✔')


login_handler = CommandHandler('login', _login_cmd, pass_args=True, pass_user_data=True)


def _logout_cmd(bot, update, user_data: dict):
    user_data.pop('rzlogin')
    bot.send_message(chat_id=update.message.chat_id,
                     text='Deine gespeicherten Login Daten wurden erfolgreich gelöscht ✔')


logout_handler = CommandHandler('logout', _logout_cmd, pass_user_data=True)
