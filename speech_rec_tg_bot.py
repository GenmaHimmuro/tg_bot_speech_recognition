from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
import traceback
import sys

from dialog_flow_response import detect_intent_texts


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    welcome = (
        f"Привет, {user.first_name}!\n"
        "Я умный бот на Dialogflow.\n"
    )
    update.message.reply_text(welcome)


def make_handle_text(dialog_flow_project_id):
    def handle_text(update: Update, context: CallbackContext):
        user_text = update.message.text.strip()
        response_text, is_fallback = detect_intent_texts(
            project_id=dialog_flow_project_id,
            session_id=f'tg-{update.effective_chat.id}',
            text=user_text
        )
        update.message.reply_text(response_text)
    return handle_text


def main():
    env = Env()
    env.read_env()
    tg_bot_token = env.str("TG_BOT_TOKEN")
    admin_chat_id_tg = env.int("ADMIN_CHAT_ID_TG")
    dialog_flow_project_id = env.str("DIALOG_FLOW_PROJECT_ID")
    try:
        updater = Updater(tg_bot_token, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, make_handle_text(dialog_flow_project_id)))
        updater.start_polling(poll_interval=1.0, timeout=10)
        updater.idle()
    except Exception as e:
        bot = Bot(token=tg_bot_token)
        error_message = f"❗ Бот упал с ошибкой:\n{e}\n\nTraceback:\n{traceback.format_exc()}"
        bot.send_message(chat_id=admin_chat_id_tg, text=error_message)
        sys.exit(1)


if __name__ == '__main__':
    main()
