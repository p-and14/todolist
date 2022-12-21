from dataclasses import dataclass, field
from typing import List, Optional

import marshmallow


@dataclass
class Entities:
    offset: int
    length: int
    type: str

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Chat:
    id: int
    first_name: str
    username: str
    type: str

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: Optional[str]
    last_name: Optional[str]
    username: str

    class Meta:
        unknown = marshmallow.EXCLUDE


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
    message: Optional[Message]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[Optional[UpdateObj]]

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = marshmallow.EXCLUDE
