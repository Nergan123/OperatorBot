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
        self._entity = {
            "text": [],
            "voice": [],
            "message": []
        }
        self.load_state()

    def set_level(self, level: int):
        """Sets sanity level"""

        self._level = level
        self.log.info(f"Setting level to {level}")
        self.save_state()

    def get_level(self):
        """Returns sanity level"""

        return self._level

    def register_entity(self, type_entity: str, ent_id: int, name: str):
        """Adds entity to the list"""

        self.log.info(f"Got\n"
                      f"\tType: {type_entity}\n"
                      f"\tID: {ent_id}\n"
                      f"\tName: {name}")

        entity = {
            "id": ent_id,
            "name": name
        }

        if entity not in self._entity[type_entity]:
            self._entity[type_entity].append(entity)
            self.log.info(f"Added {entity} to {type_entity}")
            if len(self._entity[type_entity]) > 10:
                self._entity[type_entity] = self._entity[type_entity][1::]
            self.save_state()
