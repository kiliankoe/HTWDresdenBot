import subprocess

from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode


def _start_cmd(_, update):
    update.message.reply_text(f'Hi {update.message.chat.first_name} 👋,\ntippe `/` um Vorschläge für meine möglichen '
                              f'Aktionen zu sehen. \n\nSolltest du Fragen zu einem spezifischen Befehl haben, dann '
                              f'schreibe dahinter einfach \'hilfe\' (bspws. `/raum hilfe`) um eine Erklärung dazu zu '
                              f'erhalten.',
                              parse_mode=ParseMode.MARKDOWN)


start_handler = CommandHandler('start', _start_cmd)


def _version_cmd(_, update):
    label = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])\
        .strip()\
        .decode('utf-8')
    update.message.reply_text(label)


version_handler = CommandHandler('version', _version_cmd)
