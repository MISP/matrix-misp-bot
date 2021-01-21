import logging

from nio import AsyncClient, MatrixRoom, RoomMessageText

from matrix_misp_bot.chat_functions import send_text_to_room
from matrix_misp_bot.config import Config
from matrix_misp_bot.storage import Storage

logger = logging.getLogger(__name__)


class Message:
    def __init__(
        self,
        client: AsyncClient,
        store: Storage,
        config: Config,
        message_content: str,
        room: MatrixRoom,
        event: RoomMessageText,
    ):
        """Initialize a new Message

        Args:
            client: nio client used to interact with matrix.

            store: Bot storage.

            config: Bot configuration parameters.

            message_content: The body of the message.

            room: The room the event came from.

            event: The event defining the message.
        """
        self.client = client
        self.store = store
        self.config = config
        self.message_content = message_content
        self.room = room
        self.event = event

    async def process(self) -> None:
        """Process and possibly respond to the message"""
        if self.message_content.lower() == "hello world":
            await self._hello_world()

    async def _hello_world(self) -> None:
        """Say hello"""
        text = "Hello, world!"
        await send_text_to_room(self.client, self.room.room_id, text)
