import json
import random

from discord import File

from src.operator.helpers.BaseClass import BaseClass


class LocationService(BaseClass):
    """Service responsible for location interactions"""

    SERIALIZABLE_FIELDS = [
        "_current_location"
    ]

    def __init__(self):
        super().__init__("location_service")
        self.log.info("Loaded")
        self._current_location = ""
        with open("campaign/map.json", "r") as file:
            self.map = json.loads(file.read())
        self.load_state()

    def set_location(self, location_name: str):
        """Changes current location"""

        if location_name in self.map.keys():
            self._current_location = location_name
            self.log.info(f"Setting current location to: {location_name}")
            self.save_state()
            return f"Entering {location_name}"

        raise KeyError("Location not found")

    def get_music(self, battle: bool) -> str:
        """Returns a music url"""

        if battle:
            links = self.map[self._current_location]["music_battle"]
        else:
            links = self.map[self._current_location]["music_calm"]
        output = random.choice(links)
        return output

    def get_image(self):
        """Returns a location image"""

        file_path = self.map[self._current_location]["photo"]
        self.log.info(f"Loading image {file_path}")
        image_file = File(file_path)

        return image_file

    def get_npc(self, name: str) -> dict:
        """returns an NPC dict"""

        if name not in self.map[self._current_location]["npc"]:
            raise KeyError("NPC not found")

        path = self.map[self._current_location]["npc"][name]
        with open(path, "r") as file:
            output = json.loads(file.read())

        return output
