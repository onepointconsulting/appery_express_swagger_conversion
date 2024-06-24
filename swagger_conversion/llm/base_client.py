from typing import Optional, Callable


class BaseClient:

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
        raise NotImplementedError()
