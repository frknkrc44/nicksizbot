import os
import sys
from threading import Thread

from telegram import Update
from telegram.ext import CallbackContext


def stop_and_restart(update: Update):
    # update.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)


def restart(update: Update, context: CallbackContext):
    update.message.reply_text("Bot is restarting...")
    Thread(target=stop_and_restart).start()
