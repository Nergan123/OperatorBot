from discord import File

from src.operator.helpers.BaseClass import BaseClass


class NpcService(BaseClass):
    """Service for managing NPCs"""

    SERIALIZABLE_FIELDS = [
        "_interaction"
    ]

    def __init__(self):
        super().__init__("npc_service")
        self._interaction = None
        self.load_state()
        self.log.info("Loaded")

    def load_npc(self, npc: dict) -> str:
        """Registers an ongoing interaction"""

        if not npc:
            raise KeyError("NPC not found")

        self._interaction = npc
        self.save_state()
        self.log.info(f"Recording: {npc}")

        return self._interaction["name"]

    def get_image(self):
        """Returns NPCs image"""

        if not self._interaction:
            raise KeyError("No ongoing interactions")

        self.log.info(f"Obtaining: {self._interaction['photo']}")
        image = File(self._interaction["photo"])

        return image

    def end_interaction(self):
        """Removing current npc"""

        if not self._interaction:
            raise KeyError("No ongoing interactions")

        self._interaction = None
        self.log.info("Ending interaction")
        self.save_state()
