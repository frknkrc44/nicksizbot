import configparser
import urllib.context
from telegram import *
from telegram.ext import *



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("Merhaba!")

def error(update: Update, context: CallbackContext):
    logger.warning(f'Update "{update}" caused error "{context.error}"')

def conn(url):
    return urllib.request.urlopen(url)

def gettxt(update: Update, context: CallbackContext):
    txt = update.message.text
    update.message.chat.type 
    if not bool(txt):
        txt = update.message.caption
    return txt

# Gruba yeni giren kişileri karşıla (beta)
def welcome(update: Update, context: CallbackContext):
    update.message.reply_markdown(update.message.chat.title + u" grubuna hoş geldin")


# Gruptan çıkan kişileri uğurla (beta)
def goodbye(update: Update, context: CallbackContext):
    update.message.reply_text("Hoşçakal")

# Sobet numarası belirtilen kişinin yönetici olup olmadığını bulur
def adminctrl(bot, update: Update, context: CallbackContext, id):
    for i in bot.get_chat_administrators(update.message.chat.id,context):
        if id == i.user.id:
            return True

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, goodbye))
    dp.add_handler(CommandHandler("start", start))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info('Listening...')


    updater.idle()

if __name__ == "__main__":
    main()
