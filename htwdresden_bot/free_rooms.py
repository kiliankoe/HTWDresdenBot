from datetime import datetime

from telegram.ext import CommandHandler
from telegram.chataction import ChatAction
from htwdresden import FreeRooms, Week, Day, Building, HTWBaseException


def _free_rooms_cmd(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    if len(args) == 1 and args[0].lower() == 'hilfe':
        update.message.reply_text('/raum hilft dir dabei freie Räume in der HTW zu finden. Hier ein paar '
                                  'Beispiele:\n\n'
                                  '/raum - Aktuell freie Räume im S Gebäude\n'
                                  '/raum Z - Aktuell freie Räume im Z Gebäude\n'
                                  '/raum S 13:20 - Freie Räume im S Gebäude um 13:20 Uhr\n'
                                  '/raum Z 15 - Freie Räume im Z Gebäude um 15 Uhr')
        return

    if len(args) == 0:
        building = Building.S
        time = datetime.now().strftime('%H:%M')
        time_description = 'aktuell'
    elif len(args) == 1:
        building = args[0].upper()
        time = datetime.now().strftime('%H:%M')
        time_description = 'aktuell'
    elif len(args) == 2:
        building = args[0].upper()
        time = args[1]

        # workaround for simple time syntax errors, e.g. '15' -> '15:00' or '9:20' -> '09:20'
        if ':' not in time:
            time = time + ':00'
        if len(time) == 4:
            time = '0' + time

        time_description = 'heute um {} Uhr'.format(time)
    else:
        update.message.reply_text('Das habe ich leider nicht verstanden. Tippe \'/raum hilfe\' wenn du mehr zu diesem '
                                  'Befehl erfahren willst.')
        return

    if building not in Building.all():
        update.message.reply_text('Ein solches Gebäude kenne entweder ich oder der Belegungsplan nicht. Unterstützt '
                                  'werden nur {}.'.format(', '.join(Building.all())))
        return

    try:
        rooms = FreeRooms.fetch(Week.current(), Day.current(), time, time, building)
        update.message.reply_text('Laut Belegungsplan sind folgende Räume im {} Gebäude {} frei:\n\n{}'
                                  .format(building, time_description, ', '.join(rooms)))
    except HTWBaseException:
        update.message.reply_text('Huch, mit der Anfrage gab es leider einen Fehler. 😵\nAchte bitte auf das korrekte '
                                  'Format der Uhrzeit, bspws. 13:00 oder 9:20.')


free_rooms_handler = CommandHandler('raum', _free_rooms_cmd, pass_args=True)
