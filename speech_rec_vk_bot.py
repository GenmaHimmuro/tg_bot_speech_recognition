import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from environs import Env

from dialog_flow_response import detect_intent_texts


env = Env()
env.read_env()


def main():
    vk_session = vk.VkApi(token=env.str('VK_BOT_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    project_id = env.str('DIALOG_FLOW_PROJECT_ID')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            user_text = event.text.strip()
            session_id = str(user_id)

            response_text = detect_intent_texts(
                project_id=project_id,
                session_id=session_id,
                text=user_text
            )

            if not response_text:
                response_text = "Извини, я не понял. Попробуй ещё раз!"

            vk_api.messages.send(
                user_id=user_id,
                message=response_text,
                random_id=get_random_id()
            )


if __name__ == '__main__':
    main()