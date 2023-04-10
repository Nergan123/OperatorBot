from discord import File

from src.operator.helpers.BaseClass import BaseClass


class NpcService(BaseClass):
    """Service for managing NPCs"""

    SERIALIZABLE_FIELDS = [
        "interaction",
        "_queue",
        "_turn"
    ]

    def __init__(self):
        super().__init__("npc_service")
        self.interaction = None
        self._queue = []
        self._turn = 0
        self.load_state()
        self.log.info("Loaded")

    def load_npc(self, npc: dict) -> str:
        """Registers an ongoing interaction"""

        if not npc:
            raise KeyError("NPC not found")

        self.interaction = npc
        self.save_state()
        self.log.info(f"Recording: {npc}")

        return self.interaction["name"]

    def get_name(self):
        """Returns NPC name"""

        return self.interaction["name"]

    def get_image(self):
        """Returns NPCs image"""

        if not self.interaction:
            raise KeyError("No ongoing interactions")

        self.log.info(f"Obtaining: {self.interaction['photo']}")
        image = File(self.interaction["photo"])

        return image

    def end_interaction(self):
        """Removing current npc"""

        if not self.interaction:
            raise KeyError("No ongoing interactions")

        self.interaction = None
        self._queue = []
        self._turn = 0
        self.log.info("Ending interaction")
        self.save_state()

    def set_queue(self, initiatives: list, names: list):
        """Sets a queue based on rolls"""

        initiatives, names = zip(*sorted(zip(initiatives, names)))
        self._queue = names[::-1]
        self.log.info(f"Calculated queue: {self._queue}")
        self._turn = 0
        self.save_state()
        output = self.compose_message()

        return output

    def compose_message(self):
        """Composes a message commenting on queue"""

        output = "Final turn order:\n" \
                 "```\n"
        for count, name in enumerate(self._queue):
            output += f"{count + 1}) {name}\n"
        output += "```"

        return output

    def get_turn(self):
        """Returns name on a current turn"""

        return self._queue[self._turn]

    def next_turn(self):
        """Switches to next turn"""

        self._turn += 1
        if self._turn >= len(self._queue):
            self._turn = 0

        self.save_state()
