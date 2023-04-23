import asyncio
import json
import random

from discord import File
from discord.ext.commands import Bot
from zalgo_text import zalgo

from src.operator.helpers.BaseClass import BaseClass


class SanityService(BaseClass):
    """Service to change discord appearance"""

    SERIALIZABLE_FIELDS = [
        "_level",
        "_entity"
    ]

    def __init__(self):
        super().__init__("sanity_service")
        self.log.info("Loaded")
        self._level = 0
        self._entity = []
        with open("src/data/sanity_data.json", "r") as file:
            self._data = json.loads(file.read())
        self.load_state()

    def set_level(self, level: int):
        """Sets sanity level"""

        self._level = level
        self.log.info(f"Setting level to {level}")
        self.save_state()

    def get_level(self):
        """Returns sanity level"""

        return self._level

    def register_entity(self, ent_id: int, name: str, channel_id: str):
        """Adds entity to the list"""

        self.log.info(f"Got\n"
                      f"\tID: {ent_id}\n"
                      f"\tName: {name}")

        entity = {
            "id": ent_id,
            "name": name,
            "channel": channel_id,
            "changed": False
        }

        if entity not in self._entity:
            self._entity.append(entity)
            self.log.info(f"Added {entity}")
            if len(self._entity) > 20:
                self._entity = self._entity[1::]
            self.save_state()

    async def change_entity(self, level: int, bot: Bot):
        """Changes existing entity name"""

        message = random.choice(self._entity)
        name_orig = message["name"]
        name_new = self.change_name(name_orig, level)
        channel = bot.get_channel(int(message["channel"]))
        msg = await channel.fetch_message(int(message["id"]))
        message["changed"] = True
        self.save_state()
        await msg.edit(content=name_new)

    async def restore(self, bot: Bot):
        """Restores every message to the normal state"""

        for message in self._entity:
            if message["changed"]:
                self.log.info(f"Restoring: {message}")
                name_orig = message["name"]
                channel = bot.get_channel(int(message["channel"]))
                msg = await channel.fetch_message(int(message["id"]))
                message["changed"] = False
                self.save_state()
                await msg.edit(content=name_orig)
                await asyncio.sleep(2)

    async def restore_random(self, bot: Bot):
        """Restores random message from list"""

        changed_messages = [x for x in self._entity if x["changed"]]
        if len(changed_messages) > 0:
            message = random.choice(changed_messages)
            self.log.info(f"Restoring: {message}")
            name_orig = message["name"]
            channel = bot.get_channel(int(message["channel"]))
            msg = await channel.fetch_message(int(message["id"]))
            message["changed"] = False
            self.save_state()
            await msg.edit(content=name_orig)

    def change_name(self, name: str, level: int) -> str:
        """Changes names according to sanity level"""

        self.log.info(f"Received name: {name}")
        name_new = ""
        for letter in name:
            if random.randint(0, 100) < level:
                letter = zalgo.zalgo().zalgofy(letter)
            name_new += letter

        self.log.info(f"New name: {name_new}")

        return name_new

    def get_image(self, bot: Bot):
        """Returns a random image path"""

        img = random.choice(self._data["images"])
        self.log.info(f"Returning: {img}")
        channel_id = int(self._entity[-1]["channel"])
        channel = bot.get_channel(channel_id)

        return File(img), channel

    def get_url(self):
        """Returns url from the list"""

        url = random.choice(self._data["sound"])
        self.log.info(f"Returning: {url}")

        return url
