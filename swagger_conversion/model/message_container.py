from typing import Any, Optional


class MessageContainer:
    """
    A conversation between a user and a Large Language Model (LLM) assistant.

    Holds messages and an optional metadata log (list of dicts with
    prompt information).
    """

    ROLES = ["system", "user", "assistant", "function"]

    messages: list[dict[str, str]]
    prompt_log: list[dict[str, Any]]

    def __init__(self, content: Optional[str] = None):
        """
        Initialize a new conversation.

        :param content: Initial system message (optional).
        """
        self.messages = []
        self.prompt_log = []

        if content is not None:
            self.system(content)

    @staticmethod
    def _dedent(text: str) -> str:
        """
        Remove common leading whitespace from every line of text.

        :param text: Text to dedent.
        :return: Dedented text.
        """
        indent = len(text)
        lines = text.splitlines()
        for line in lines:
            if line.strip():
                indent = min(indent, len(line) - len(line.lstrip()))
        dedented_lines = [line[indent:].rstrip() for line in lines]
        return "\n".join(line for line in dedented_lines)

    def add(
        self, role: str, content: str, name: Optional[str] = None
    ) -> "MessageContainer":
        """
        Add a message to the conversation.

        In most cases, you should use the convenience methods instead.

        :param role: Role of the message (system, user, assistant, function).
        :param content: Content of the message.
        :param name: Name of the message sender (optional).
        :return: The conv object.
        """

        if role not in self.ROLES:
            raise ValueError(f"Unknown role: {role}")
        if not content:
            raise ValueError("Empty message content")
        if not isinstance(content, str) and not isinstance(content, dict):
            raise TypeError(f"Invalid message content: {type(content).__name__}")

        message = {
            "role": role,
            "content": self._dedent(content) if isinstance(content, str) else content,
        }
        if name is not None:
            message["name"] = name

        self.messages.append(message)
        return self

    def system(self, content: str, name: Optional[str] = None) -> "MessageContainer":
        """
        Add a system message to the conversation.

        System messages can use `name` for showing example conversations
        between an example user and an example assistant.

        :param content: Content of the message.
        :param name: Name of the message sender (optional).
        :return: The convo object.
        """
        return self.add("system", content, name)

    def user(self, content: str, name: Optional[str] = None) -> "MessageContainer":
        """
        Add a user message to the conversation.

        :param content: Content of the message.
        :param name: User name (optional).
        :return: The convo object.
        """
        return self.add("user", content, name)

    def function(self, content: str, name: Optional[str] = None) -> "Convo":
        """
        Add a function (tool) response to the conversation.

        :param content: Content of the message.
        :param name: Function/tool name (optional).
        :return: The convo object.
        """
        return self.add("function", content, name)
