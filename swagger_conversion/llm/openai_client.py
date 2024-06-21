from typing import Optional, Callable, List, Dict
from openai import AsyncOpenAI
from httpx import Timeout

from swagger_conversion.config import cfg
from swagger_conversion.model.message_container import MessageContainer


class OpenAIClient:

    def __init__(
        self,
        *,
        stream_handler: Optional[Callable] = None,
        error_handler: Optional[Callable] = None,
    ):
        """
        Initialize the client with the given configuration.

        :param config: Configuration for the client.
        :param stream_handler: Optional handler for streamed responses.
        """
        self.stream_handler = stream_handler
        self.error_handler = error_handler
        self._init_client()

    def _init_client(self):
        connect_timeout = cfg.connect_timeout
        read_timeout = cfg.read_timeout
        self.client = AsyncOpenAI(
            api_key=cfg.openai_api_key,
            timeout=Timeout(
                max(connect_timeout, read_timeout),
                connect=connect_timeout,
                read=read_timeout,
            ),
        )

    async def make_request(
        self,
        convo: MessageContainer,
        json_mode: bool = False,
        functions: Optional[List[Dict]] = None,
        function_call: Optional[str] = "auto"
    ) -> tuple[str, int, int]:
        completion_kwargs = {
            "model": cfg.openai_api_model,
            "messages": convo.messages,
            "temperature": cfg.openai_api_temperature,
            "stream": True,
            "stream_options": {
                "include_usage": True,
            },
        }
        if functions is not None:
            completion_kwargs["functions"] = functions
            completion_kwargs["function_call"] = function_call
            completion_kwargs["response_format"] = {"type": "json_object"}
        if json_mode:
            completion_kwargs["response_format"] = {"type": "json_object"}

        stream = await self.client.chat.completions.create(**completion_kwargs)
        response = []
        prompt_tokens = 0
        completion_tokens = 0

        async for chunk in stream:
            if chunk.usage:
                prompt_tokens += chunk.usage.prompt_tokens
                completion_tokens += chunk.usage.completion_tokens

            if not chunk.choices:
                continue

            if functions and chunk.choices[0].delta.function_call:
                content = chunk.choices[0].delta.function_call.arguments
            else:
                content = chunk.choices[0].delta.content

            if not content:
                continue

            response.append(content)
            if self.stream_handler:
                await self.stream_handler(content)

        response_str = "".join(response)

        # Tell the stream handler we're done
        if self.stream_handler:
            await self.stream_handler(None)

        return response_str, prompt_tokens, completion_tokens
