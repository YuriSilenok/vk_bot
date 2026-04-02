from threading import Thread
from typing import List, Optional

from fastapi import FastAPI
import uvicorn
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

from .router import Router
from .message import Message


class Bot:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, token: str, group_id: int):
        self.token = token
        self.group_id = group_id
        self.routers: List[Router] = []

        self.session = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.session, group_id)
        self.vk = self.session.get_api()

    @classmethod
    def get_instance(cls):
        """Получить экземпляр (если не инициализирован - вернет None)"""
        return cls._instance

    def include_router(self, router: Router):
        self.routers.append(router)

    def _extract_message_data(self, event) -> Message:
        """
        Извлекает данные из события VK и преобразует в объект Message
        """
        msg = event.message

        # Создаем объект сообщения с удобными полями для фильтрации
        return Message(
            bot=self,
            text=msg.get('text', ''),
            from_id=msg.get('from_id', 0),
            peer_id=msg.get('peer_id', 0),
            date=msg.get('date', 0),
            payload=msg.get('payload', {}),
            attachments=msg.get('attachments', [])
        )

    def _listen(self):
        for event in self.longpoll.listen():
            message: Message = self._extract_message_data(event)
            for router in self.routers:
                result = router.process(message)
                if result is not None:
                    break

    def run(self, app: Optional[FastAPI] = None):

        if app:
            Thread(target=self._thread_run, daemon=True).start()
            uvicorn.run(app, host="127.0.0.1", port=8012, log_level="info")
        else:
            self._listen()
