import json

import marshmallow_dataclass
import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


GetUpdateSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
SendMessageSchema = marshmallow_dataclass.class_schema(SendMessageResponse)


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url("getUpdates")
        params = {"offset": offset, "timeout": timeout}

        r = requests.get(url=url, params=params)
        j = json.loads(r.text)
        return GetUpdateSchema().load(j)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url("sendMessage")
        params = {"chat_id": chat_id, "text": text}

        r = requests.get(url=url, params=params)
        j = json.loads(r.text)
        return SendMessageSchema().load(j)
