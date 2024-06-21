from swagger_conversion.test.provider.message_convo_provider import (
    create_message_container,
)


def test_config_values():
    message_container = create_message_container()
    assert message_container is not None
    messages = message_container.messages
    assert messages is not None
    assert len(messages) == 2
    assert messages[0] is not None
    assert messages[0]["role"] is not None
    assert messages[0]["role"] == "system"
