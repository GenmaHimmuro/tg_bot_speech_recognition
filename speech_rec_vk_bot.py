import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from environs import Env
import traceback
from telegram import Bot
import sys

from dialog_flow_response import detect_intent_texts


env = Env()
env.read_env()

ADMIN_CHAT_ID_TG = env.int("ADMIN_CHAT_ID_TG")
TG_BOT_TOKEN = env.str("TG_BOT_TOKEN")
PROJECT_ID = env.str('DIALOG_FLOW_PROJECT_ID')


def main():
    vk_session = vk.VkApi(token=env.str('VK_BOT_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = event.user_id
                user_text = event.text.strip()
                session_id = str(user_id)
                
                response_text, is_fallback = detect_intent_texts(
                    project_id=PROJECT_ID,
                    session_id=session_id,
                    text=user_text
                )
                if not is_fallback and response_text:
                    vk_api.messages.send(
                        user_id=user_id,
                        message=response_text,
                        random_id=get_random_id()
                    )
    except Exception as e:
        bot = Bot(token=TG_BOT_TOKEN)
        error_message = f"❗ VK бот упал с ошибкой:\n{e}\n\nTraceback:\n{traceback.format_exc()}"
        bot.send_message(chat_id=ADMIN_CHAT_ID_TG, text=error_message)
        sys.exit(1)


if __name__ == '__main__':
    main()