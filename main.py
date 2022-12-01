import time

import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
import config


if __name__ == '__main__':
    session = requests.Session()
    login, password = config.login, config.password
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
    time.sleep(10)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            # Слушаем longpoll, если пришло сообщение то:
            if 'Время просмотра анкеты истекло' in event.text or event.text == 'Второй вариант фразы':  # Если написали заданную фразу
                if event.from_user:  # Если написали в ЛС
                    vk.messages.send(  # Отправляем сообщение
                        user_id=event.user_id,
                        message='Ваш текст'
                    )
                elif event.from_chat:  # Если написали в Беседе
                    vk.messages.send(  # Отправляем собщение
                        chat_id=event.chat_id,
                        message='Ваш текст'
                    )