from typing import Optional, List, Dict

from anthropic import Anthropic, AsyncAnthropic, RateLimitError
from anthropic.types import ToolParam, MessageParam

from httpx import Timeout

from swagger_conversion.llm.base_client import BaseClient
from swagger_conversion.config import cfg
from swagger_conversion.model.message_container import MessageContainer

# Maximum number of tokens supported by Anthropic Claude 3
MAX_TOKENS = 4096

class AnthropicClient(BaseClient):

    def _init_client(self):
        connect_timeout = cfg.connect_timeout
        read_timeout = cfg.read_timeout
        self.client = AsyncAnthropic(
            api_key=cfg.anthropic_api_key,
            timeout=Timeout(
                max(connect_timeout, read_timeout),
                connect=connect_timeout,
                read=read_timeout,
            ),
        )
        self.stream_handler = self.stream_handler

    @staticmethod
    def _adapt_messages(convo: MessageContainer) -> list[dict[str, str]]:
        """
        Adapt the conversation messages to the format expected by the Anthropic Claude model.

        Claude only recognizes "user" and "assistant" roles, and requires them to be switched
        for each message (ie. no consecutive messages from the same role).

        :param convo: Conversation to adapt.
        :return: Adapted conversation messages.
        """
        messages = []
        for msg in convo.messages:
            if msg["role"] == "function":
                raise ValueError("Anthropic Claude doesn't support function calling, but it supports tools")

            role = "user" if msg["role"] in ["user", "system"] else "assistant"
            if messages and messages[-1]["role"] == role:
                messages[-1]["content"] += "\n\n" + msg["content"]
            else:
                messages.append(
                    {
                        "role": role,
                        "content": msg["content"],
                    }
                )
        return messages


    async def make_request(
        self,
        convo: MessageContainer,
        json_mode: bool = False,
        tools: Optional[List[ToolParam]] = None,
    ) -> tuple[str, int, int]:
        convo.messages = AnthropicClient._adapt_messages(convo)
        completion_kwargs = {
            "max_tokens": MAX_TOKENS,
            "model": cfg.anthropic_model,
            "messages": convo.messages,
            "temperature": cfg.openai_api_temperature,
        }
        if json_mode:
            completion_kwargs["response_format"] = {"type": "json_object"}

        response = []
        async with self.client.messages.stream(**completion_kwargs) as stream:
            async for content in stream.text_stream:
                response.append(content)
                if self.stream_handler:
                    await self.stream_handler(content)

            # TODO: get tokens from the final message
            final_message = await stream.get_final_message()
            final_message.content

        response_str = "".join(response)

        # Tell the stream handler we're done
        if self.stream_handler:
            await self.stream_handler(None)

        return response_str, final_message.usage.input_tokens, final_message.usage.output_tokens