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
#from core.actionwraps.actionwraps import restricted, send_typing_action
# Core - echo
#from core.echo.echo_functions import echo
# Core - restart action
#from core.grace_restart.restart_functions import restart
# Core - Logger
#from core.tglog.tglogger import tgkatlogger
# Extensions - welcome
#from extensions.welcome.welcome_functions import hello

import importlib
import os
import inspect

part_names = []

# Add all of modules
def add_modules():
    CWD = os.getcwd()
    for dirs in os.listdir(CWD):
        dirpath = CWD + "/" + dirs
        if os.path.isdir(dirpath) and dirs != "__pycache__" and dirs[0] != ".":
            for subdirs in os.listdir(dirpath):
                subdirpath = dirpath + "/" + subdirs
                if os.path.isdir(subdirpath) and subdirs != "__pycache__" and dirs[0] != ".":
                    for files in os.listdir(subdirpath):
                        if(os.path.isfile(subdirpath + "/" + files) and
                             files[-3:] ==".py" and files != "__init__.py"):
                            submod = files[:-3]
                            module = dirs + "." + subdirs +"." + submod
                            impt = importlib.import_module(module)
                            setattr(sys.modules[__name__],submod,impt)
                            for mod in inspect.getmembers(impt,inspect.isfunction):
                                part_names.append(mod)

add_modules()

"""
def _is_method(func):
    spec = inspect.getargspec(func)
    return spec.args and spec.args[0] == 'self'
"""

@actionwraps.restricted
def state(context: CallbackContext, update):
    sleep(1)
    update.message.reply_text("Ok")
    return ConversationHandler.END


@actionwraps.send_typing_action
def start(update, context):
    update.message.reply_text("Instant change!")


def error(update: Update, context: CallbackContext):
    tglogger.warning(f'Update "{update}" caused error "{context.error}"')


def gettxt(update: Update, context: CallbackContext):
    txt = update.message.text
    update.message.chat.type
    if not bool(txt):
        txt = update.message.caption
    return txt


# Gruba yeni giren kişileri karşıla (beta)
@actionwraps.send_typing_action
def welcome(update: Update, context: CallbackContext):
    update.message.reply_markdown(update.message.chat.title + " grubuna hoş geldin")


# Gruptan çıkan kişileri uğurla (beta)
@actionwraps.send_typing_action
def goodbye(update: Update, context: CallbackContext):
    update.message.reply_text("Hoşçakal")

def add_cmds(dp):
    for module in part_names:
        dp.add_handler(CommandHandler(module[0],module[1]))

def main():
    try:
        updater = Updater(kconfig.TOKEN, use_context=True)
        dp = updater.dispatcher
        add_cmds(dp)
        dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
        dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, goodbye))
        dp.add_handler(CommandHandler("kstart", start))
        dp.add_handler(CommandHandler("state", state))
        """
        dp.add_handler(CommandHandler("hello", welcome_functions.hello))
        dp.add_handler(
            CommandHandler("rb", restart_functions.restart, filters=Filters.user(username=kconfig.OWNER))
        )
        """
        dp.add_error_handler(error)
        updater.start_polling()
        updater.idle()
    except KeyboardInterrupt:
        updater.stop()

if __name__ == "__main__":
    main()
