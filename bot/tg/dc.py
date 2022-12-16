from dataclasses import dataclass, field
from typing import List, Optional

import marshmallow
import marshmallow_dataclass


@dataclass
class Entities:
    offset: int
    length: int
    type: str


@dataclass
class Chat:
    id: int
    first_name: str
    username: str
    type: str


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: Optional[str]


@dataclass
class Message:
    message_id: int
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat
    date: int
    text: Optional[str]
    entities: Optional[List[Entities]]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class UpdateObj:
    update_id: int
    message: Message

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[Optional[UpdateObj]]
    error_code: Optional[int]
    description: Optional[str]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = marshmallow.EXCLUDE
