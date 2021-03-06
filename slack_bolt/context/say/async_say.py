from typing import Optional, List, Union, Dict

from slack_bolt.context.say.internals import _can_say
from slack_sdk.models.attachments import Attachment
from slack_sdk.models.blocks import Block
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.web.async_slack_response import AsyncSlackResponse


class AsyncSay:
    client: Optional[AsyncWebClient]
    channel: Optional[str]

    def __init__(
        self, client: Optional[AsyncWebClient], channel: Optional[str],
    ):
        self.client = client
        self.channel = channel

    async def __call__(
        self,
        text: Union[str, dict] = "",
        blocks: Optional[List[Union[Dict, Block]]] = None,
        attachments: Optional[List[Union[Dict, Attachment]]] = None,
        channel: Optional[str] = None,
    ) -> AsyncSlackResponse:
        if _can_say(self, channel):
            text_or_whole_response: Union[str, dict] = text
            if isinstance(text_or_whole_response, str):
                text = text_or_whole_response
                return await self.client.chat_postMessage(
                    channel=channel or self.channel,
                    text=text,
                    blocks=blocks,
                    attachments=attachments,
                )
            elif isinstance(text_or_whole_response, dict):
                message: dict = text_or_whole_response
                if "channel" not in message:
                    message["channel"] = channel or self.channel
                return await self.client.chat_postMessage(**message)
            else:
                raise ValueError(
                    f"The arg is unexpected type ({type(text_or_whole_response)})"
                )
        else:
            raise ValueError("say without channel_id here is unsupported")
