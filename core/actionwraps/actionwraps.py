from functools import wraps

from telegram import ChatAction, Update
from telegram.ext import CallbackContext


def send_typing_action(func):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return command_func


def restricted(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):
        user_id = update.message.from_user.id
        print()
        print()
        print()
        print()
        objt = context.bot.get_chat_administrators(update.message.chat.id)
        for attr in objt:
            type(attr)
            # print(attr, getattr(objt, attr))
            print(attr)
            print("---------------------------------")

        print()
        print()
        print()
        print()
        print()
        print()

        if user_id not in context.bot.get_chat_administrators(update.message.chat.id):
            print()
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)

    return wrapped
