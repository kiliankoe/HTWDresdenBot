from datetime import datetime, timedelta

from telegram.ext import CommandHandler
from telegram.parsemode import ParseMode
from telegram.chataction import ChatAction

from htwdresden import Meal, Canteen


DEFAULT_CANTEEN_NAME = 'Mensa Reichenbachstraße'
DEFAULT_CANTEEN_ID = 1
DEFAULT_DATE = datetime.now()


def _meals_cmd(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    if len(args) == 0:
        # /mensa
        canteen_name = None
        date = None
    elif len(args) == 1:
        # /mensa heute OR /mensa Alte Mensa
        if args[0].lower() == 'heute':
            canteen_name = None
            date = datetime.now()
        elif args[0].lower() == 'morgen':
            canteen_name = None
            date = datetime.now() + timedelta(days=1)
        elif args[0].lower() == 'übermorgen' or args[0].lower() == 'uebermorgen':
            canteen_name = None
            date = datetime.now() + timedelta(days=2)
        else:
            canteen_name = args[0]
            date = None
    else:
        # /mensa Alte Mensa heute OR /mensa Siedepunkt 2018-04-15
        canteen_name = args

        # canteen_name = args[0]
        if args[-1].lower() == 'heute':
            canteen_name = canteen_name[:-1]
            date = datetime.now()
        elif args[-1].lower() == 'morgen':
            canteen_name = canteen_name[:-1]
            date = datetime.now() + timedelta(days=1)
        elif args[-1].lower() == 'übermorgen' or args[-1].lower() == 'uebermorgen':
            canteen_name = canteen_name[:-1]
            date = datetime.now() + timedelta(days=2)
        else:
            date = DEFAULT_DATE

        canteen_name = ' '.join(canteen_name)

    if canteen_name is None:
        canteen_name = DEFAULT_CANTEEN_NAME
        canteen_id = DEFAULT_CANTEEN_ID
    else:
        canteen_name = _common_canteen_names(canteen_name)
        all_canteens = Canteen.fetch_all()
        canteen_id = 0
        for c in all_canteens:
            if c.name.lower() == canteen_name.lower():
                canteen_name = c.name
                canteen_id = c.id
        if canteen_id == 0:
            update.message.reply_text('Ich konnte leider keine Mensa mit dem Namen {} finden. 😢'.format(canteen_name))
            return

    if date is None:
        date = DEFAULT_DATE

    meals = Meal.fetch(canteen_id, date.strftime('%Y-%m-%d'))

    if len(meals) == 0:
        update.message.reply_text('Am {} gibt\'s leider nichts @ {} 😕'
                                  .format(date.strftime('%d.%m.%Y'), canteen_name))
        return

    update.message.reply_text('Am {} gibt\'s @ {}:\n\n{}'
                              .format(date.strftime('%d.%m.%Y'),
                                      canteen_name,
                                      '\n'.join([_format_meal(m) for m in meals])),
                              parse_mode=ParseMode.MARKDOWN)


meals_handler = CommandHandler('mensa', _meals_cmd, pass_args=True)


def _format_meal(meal: Meal) -> str:
    if meal.student_price is not None and meal.student_price != 0:
        return ' - {} {:.2f}€'.format(meal.title, meal.student_price)
    else:
        return ' - {}'.format(meal.title)


def _common_canteen_names(name: str) -> str:
    if name in ["alte", "mommsa", "brat2", "bratquadrat"]:
        return 'Alte Mensa'
    elif name in ["uboot", "bio", "biomensa"]:
        return 'BioMensa U-Boot'
    elif name in ["brühl", "bruehl", "hfbk"]:
        return 'Mensa Brühl'
    elif name in ["görlitz", "goerlitz"]:
        return 'Mensa Görlitz'
    elif name in ["jotown", "ba"]:
        return 'Mensa Johannstadt'
    elif name in ["palucca", "tanz"]:
        return 'Mensa Palucca Hochschule'
    elif name in ["reichenbach", "htw", "reiche", "club mensa"]:
        return 'Mensa Reichenbachstraße'
    elif name in ["siede", "siedepunkt", "drepunct", "drehpunkt", "siedepunct", "slub"]:
        return 'Mensa Siedepunkt'
    elif name in ["stimmgabel", "hfm", "musik", "musikhochschule"]:
        return 'Mensa Stimmgabel'
    elif name in ["tharandt", "tellerrand"]:
        return 'Mensa Tellerrandt'
    elif name in ["wu", "wu1", "wundtstraße"]:
        return 'Mensa WuEins'
    elif name in ["zelt", "zeltmensa", "schlösschen", "feldschlösschen", "neue"]:
        return 'Zeltschlösschen'
    elif name in ["grill", "cube", "grillcube"]:
        return 'Grill Cube'
    else:
        return name


def _meal_search_cmd(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    if len(args) == 0:
        update.message.reply_text('Für eine Suche benötige ich mindestens einen Suchbegriff.')
        return

    query = ' '.join(args)

    meals = Meal.search(query)
    meals = sorted(meals, key=lambda m: m.canteen)

    if len(meals) == 0:
        update.message.reply_text('Für \'{}\' habe ich leider keine Treffer gefunden. 😕'
                                  .format(query))
        return

    update.message.reply_text('Meine Suche ergab folgende Treffer:\n\n- {}'
                              .format('\n- '.join([_format_search_results(m) for m in meals])),
                              parse_mode=ParseMode.MARKDOWN)


meal_search_handler = CommandHandler('mensasuche', _meal_search_cmd, pass_args=True)


def _format_search_results(meal: Meal) -> str:
    date = datetime.strptime(meal.date, '%Y-%m-%d').strftime('%d.%m.%Y')
    title = meal.title
    canteen = meal.canteen

    return "{} @ {}: {}".format(date, canteen, title)
