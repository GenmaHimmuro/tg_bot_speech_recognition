from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env

from dialog_flow_response import detect_intent_texts


env = Env()
env.read_env()


TG_BOT_TOKEN = env.str("TG_BOT_TOKEN")
DIALOG_FLOW_PROJECT_ID = env.str("DIALOG_FLOW_PROJECT_ID")


def get_session_id(update: Update) -> str:
    return str(update.effective_chat.id)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    welcome = (
        f"Привет, {user.first_name}!\n"
        "Я умный бот на Dialogflow.\n"
    )
    update.message.reply_text(welcome)


def handle_text(update: Update, context: CallbackContext):
    user_text = update.message.text.strip()
    session_id = get_session_id(update)

    response_text, is_fallback = detect_intent_texts(
        project_id=DIALOG_FLOW_PROJECT_ID,
        session_id=session_id,
        text=user_text
    )
    update.message.reply_text(response_text)


def main():
    print("Запуск бота с Dialogflow...")

    updater = Updater(TG_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling(poll_interval=1.0, timeout=10)
    updater.idle()


if __name__ == '__main__':
    main()
