import asyncio
from swagger_conversion.test.provider.message_convo_provider import (
    create_message_container,
)
from swagger_conversion.llm.openai_client import OpenAIClient


def test_make_request():
    message_container = create_message_container()
    api = OpenAIClient()
    response = asyncio.run(api.make_request(message_container))
    assert response is not None
    print("OpenAI response", response[0])
