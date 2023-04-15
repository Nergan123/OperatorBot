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
        self._entity = {}
        self.load_state()

    def set_level(self, level: int):
        """Sets sanity level"""

        self._level = level
        self.log.info(f"Setting level to {level}")
        self.save_state()

    def get_level(self):
        """Returns sanity level"""

        return self._level

    def register_entity(self, type_entity: str, name: str):
        """Adds entity to the list"""

        if isinstance(self._entity[type_entity], list):
            self._entity[type_entity] = self._entity[type_entity].append(name)
        else:
            self._entity[type_entity] = []
            self._entity[type_entity] = self._entity[type_entity].append(name)

        self.log.info(f"Added {name} to {type_entity}")
        self.save_state()
