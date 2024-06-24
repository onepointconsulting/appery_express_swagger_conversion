import asyncio
from swagger_conversion.test.provider.message_convo_provider import (
    create_message_container,
)
from swagger_conversion.llm.anthropic_client import AnthropicClient


def test_make_request():
    message_container = create_message_container()
    api = AnthropicClient()
    response = asyncio.run(api.make_request(message_container))
    assert response is not None
    print("Anthropic response", response[0])
