from nio import AsyncClient, MatrixRoom, RoomMessageText

from matrix_misp_bot.chat_functions import react_to_event, send_text_to_room
from matrix_misp_bot.config import Config
from matrix_misp_bot.storage import Storage

from pymisp import PyMISP


class Command:
    def __init__(
        self,
        client: AsyncClient,
        store: Storage,
        config: Config,
        command: str,
        room: MatrixRoom,
        event: RoomMessageText,
    ):
        """A command made by a user.

        Args:
            client: The client to communicate to matrix with.

            store: Bot storage.

            config: Bot configuration parameters.

            command: The command and arguments.

            room: The room the command was sent in.

            event: The event describing the command.
        """
        self.client = client

        self.store = store
        self.config = config
        self.command = command
        self.room = room
        self.event = event
        self.args = self.command.split()[1:]

        self.pymisp = PyMISP(self.config.config_dict.get('misp')['url'],
                             self.config.config_dict.get('misp')['apikey'])
        self.allowed_users = self.config.config_dict.get('misp')['allowed_users']
        self.allowed_servers = self.config.config_dict.get('misp')['allowed_servers']

    async def process(self):
        """Process the command"""
        if self.command.startswith("misp"):
            await self._misp()
        elif self.command.startswith("echo"):
            await self._echo()
        elif self.command.startswith("react"):
            await self._react()
        elif self.command.startswith("help"):
            await self._show_help()
        else:
            await self._unknown_command()

    async def _misp(self):
        for user in self.room.users.keys():
            if user in self.allowed_users:
                continue
            if user.split(':', 1)[-1] in self.allowed_servers:
                continue
            response = 'Not allowed.'
            break
        else:
            if self.args[0] == 'search':
                attrs = self.pymisp.search(controller='attributes', value=self.args[1], page=1, limit=20, pythonify=True)
                if attrs:
                    response = 'The following events contain this value: \n'
                    for a in attrs:
                        response += f'{self.pymisp.root_url}/events/view/{a.event_id}\n'
                else:
                    response = 'Nothing found.'
            else:
                response = 'Only "search" is supported for now.'
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _echo(self):
        """Echo back the command's arguments"""
        response = " ".join(self.args)
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _react(self):
        """Make the bot react to the command message"""
        # React with a start emoji
        reaction = "⭐"
        await react_to_event(
            self.client, self.room.room_id, self.event.event_id, reaction
        )

        # React with some generic text
        reaction = "Some text"
        await react_to_event(
            self.client, self.room.room_id, self.event.event_id, reaction
        )

    async def _show_help(self):
        """Show the help text"""
        if not self.args:
            text = (
                "Hello, I am a bot made with matrix-nio! Use `help commands` to view "
                "available commands."
            )
            await send_text_to_room(self.client, self.room.room_id, text)
            return

        topic = self.args[0]
        if topic == "rules":
            text = "These are the rules!"
        elif topic == "commands":
            text = "Available commands: ..."
        else:
            text = "Unknown help topic!"
        await send_text_to_room(self.client, self.room.room_id, text)

    async def _unknown_command(self):
        await send_text_to_room(
            self.client,
            self.room.room_id,
            f"Unknown command '{self.command}'. Try the 'help' command for more information.",
        )