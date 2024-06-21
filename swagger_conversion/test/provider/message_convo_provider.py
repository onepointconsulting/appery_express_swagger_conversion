from swagger_conversion.model.message_container import MessageContainer


def create_message_container() -> MessageContainer:
    container = MessageContainer("You are a helpful assistant")
    container.user(
        'Certainly! Below is a simple Swagger (OpenAPI) definition for a "Hello World" API. This API will have a single endpoint that returns a "Hello, World!" message.'
    )
    return container
