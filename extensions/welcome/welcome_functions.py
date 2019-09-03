import telegram
from telegram import Update

new_value = "hello let us see if it is exists"


def hello(update: Update, context):
    update.message.reply_text(
        text="<code>%s</code>" % (new_value), parse_mode=telegram.ParseMode.HTML
    )
