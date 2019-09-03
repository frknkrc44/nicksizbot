import configparser
import sys
from time import sleep

import requests
import telegram
from telegram import *
from telegram.ext import *

# Kat Bot Settings
import kat_config as kconfig
# Core - send typing action
from core.actionwraps.actionwraps import restricted, send_typing_action
# Core - echo
from core.echo.echo_functions import echo
# Core - restart action
from core.grace_restart.restart_functions import restart
# Core - Logger
from core.tglog.tglogger import tgkatlogger
# Extensions - welcome
from extensions.welcome.welcome_functions import hello


@restricted
def state(context: CallbackContext, update):
    sleep(1)
    update.message.reply_text("Ok")
    return ConversationHandler.END


@send_typing_action
def start(update, context):
    update.message.reply_text("Instant change!")


def error(update: Update, context: CallbackContext):
    tgkatlogger.warning(f'Update "{update}" caused error "{context.error}"')


def gettxt(update: Update, context: CallbackContext):
    txt = update.message.text
    update.message.chat.type
    if not bool(txt):
        txt = update.message.caption
    return txt


# Gruba yeni giren kişileri karşıla (beta)
@send_typing_action
def welcome(update: Update, context: CallbackContext):
    update.message.reply_markdown(update.message.chat.title + " grubuna hoş geldin")


# Gruptan çıkan kişileri uğurla (beta)
@send_typing_action
def goodbye(update: Update, context: CallbackContext):
    update.message.reply_text("Hoşçakal")


def main():
    try:
        updater = Updater(kconfig.TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
        dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, goodbye))
        dp.add_handler(CommandHandler("kstart", start))
        dp.add_handler(CommandHandler("hello", hello))
        dp.add_handler(CommandHandler("state", state))
        dp.add_handler(
            CommandHandler("rb", restart, filters=Filters.user(username=kconfig.OWNER))
        )
        dp.add_error_handler(error)
        updater.start_polling()
        updater.idle()
    except KeyboardInterrupt:
        updater.stop()


if __name__ == "__main__":
    main()
