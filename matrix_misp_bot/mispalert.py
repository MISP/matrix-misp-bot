import logging
from datetime import datetime
from pathlib import Path
from typing import List

from nio import AsyncClient
from pymisp import MISPEvent, PyMISP

from matrix_misp_bot.chat_functions import send_text_to_room
from matrix_misp_bot.config import Config
from matrix_misp_bot.storage import Storage

logger = logging.getLogger(__name__)


class MISPAlert:
    """"""

    def __init__(self, client: AsyncClient, config: Config, store: Storage):
        self.client = client
        self.config = config
        self.store = store

        self.pymisp = PyMISP(self.config.config_dict.get('misp')['url'],
                             self.config.config_dict.get('misp')['apikey'])
        self.allowed_users = self.config.config_dict.get('misp')['allowed_users']
        self.allowed_servers = self.config.config_dict.get('misp')['allowed_servers']
        self.alert_tags = self.config.config_dict.get('misp')['alert_tags']
        last_alert = self.pymisp.search(controller='events', tags=self.alert_tags, limit=1, page=1, pythonify=True, metadata=True, order='Event.timestamp desc')
        if last_alert:
            self.last_alert_ts = last_alert[0].timestamp
        else:
            self.last_alert_ts = datetime.min
        logger.debug(f"Most recent alert: {self.last_alert_ts}")

    async def alerter(self):
        """Query MISP and find the new alert notifications to send"""
        # get rooms
        rooms_to_update = self._authorized_subscribers()
        if rooms_to_update:
            # get the last 10 entries with this tag
            events = self.pymisp.search(controller='events', tags=self.alert_tags, limit=10, page=1, pythonify=True, order='Event.timestamp desc')
            to_post = [event for event in events if event.timestamp > self.last_alert_ts]
            if to_post:
                self.last_alert_ts = to_post[0].timestamp
                await self._update_rooms(rooms_to_update, to_post)
            else:
                logger.debug("No alerts.")
        else:
            logger.debug("No authorized rooms found.")

    def _authorized_subscribers(self):
        to_return = []
        if not (Path(__file__).parent / 'subscribed').exists():
            return to_return
        with open(Path(__file__).parent / 'subscribed') as f_ro:
            subscribed = [roomid.strip() for roomid in f_ro.readlines()]
        for room_id, room in self.client.rooms.items():
            for user in room.users.keys():
                if user in self.allowed_users:
                    continue
                if user.split(':', 1)[-1] in self.allowed_servers:
                    continue
                break
            else:
                # All the users in the room are authorized
                if room_id in subscribed:
                    to_return.append(room_id)
        return to_return

    async def _update_rooms(self, rooms_to_update: List[str], alerts: List[MISPEvent]):
        """Posts the alerts in the rooms

        Args:
            alerts: A list of alerts

        """
        logger.debug("Updating rooms...")
        message = "New alert(s):"
        for alert in alerts:
            message += f'\n\t{alert.info}: {self.pymisp.root_url}/events/view/{alert.id}'

        for room_id in rooms_to_update:
            await send_text_to_room(self.client, room_id, message)
