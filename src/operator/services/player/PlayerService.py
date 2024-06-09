from dataclasses import asdict

from discord.ext.commands import Context

from src.operator.helpers.BaseClass import BaseClass
from src.player.PlayerData import PlayerData


class PlayerService(BaseClass):
    """Class to handle players"""

    SERIALIZABLE_FIELDS = [
        "_players"
    ]

    def __init__(self):
        super().__init__("player_service")
        self._players = {}
        self.load_state()

    def add_player(self, ctx: Context, name: str) -> None:
        """Adds player to list"""

        self.log.info(self._players.keys())
        if str(ctx.message.author.id) in self._players.keys():
            raise KeyError("Player already exists")

        self._players[str(ctx.message.author.id)] = asdict(PlayerData(ctx, name))
        self.save_state()

    def remove_player(self, player_id: int) -> None:
        """Removes player object"""

        self._players.pop(player_id)
        self.save_state()

    def set_parameter(self, player_id: int, parameter_name: str, parameter_val: int | str) -> None:
        """Sets a parameter in player object"""

        self._players[player_id][parameter_name] = parameter_val
        self.log.debug(self._players)
        self.save_state()

    def get_player_id_by_name(self, name: str) -> int:
        """Returns a player id"""

        for player_id in self._players:
            self.log.debug(player_id)
            if self._players[player_id]["name"] == name:
                return player_id

        raise ValueError("Player name not found")

    def get_player_by_id(self, player_id: int) -> dict:
        """Returns player object"""

        return self._players[str(player_id)]

    def get_player_by_name(self, name: str) -> dict:
        """Returns player object"""

        player_id = self.get_player_id_by_name(name)
        return self._players[player_id]

    def get_players(self):
        """Returns all players"""

        players = []
        for player in self._players:
            players.append(self._players[player])
        self.log.info(f"Returning: {players}")

        return players

    def set_initiative(self, name: str, val: int):
        """Sets modifier"""

        player_id = self.get_player_id_by_name(name)
        self.log.info(f"Setting {val} for {name}")

        self._players[player_id]["initiative"] = val
        self.save_state()

    def add_item(self, name: str, item: str, quantity: int):
        """Adds an item to player"""

        player_id = self.get_player_id_by_name(name)
        self.log.info(f"Adding {item} to {name}")

        if len(self._players[player_id]["items"]) >= 9:
            raise ValueError("Player has too many items")

        self._players[player_id]["items"].append({"name": item, "quantity": quantity})
        self.save_state()

    def edit_item(self, name: str, item_name: str, quantity: int):
        """Edits an item in player"""

        player_id = self.get_player_id_by_name(name)
        self.log.info(f"Editing {item_name} in {name}")

        for item in self._players[player_id]["items"]:
            if quantity == 0 and item["name"] == item_name:
                self._players[player_id]["items"].remove(item)
                break
            if item["name"] == item_name:
                item["quantity"] = quantity
                break
        self.save_state()

    def remove_item(self, name: str, item_name: str):
        """Removes an item from player"""

        player_id = self.get_player_id_by_name(name)
        self.log.info(f"Removing {item_name} from {name}")
        self.log.debug(self._players[player_id]["items"])

        for item in self._players[player_id]["items"]:
            if item["name"] == item_name:
                self._players[player_id]["items"].remove(item)
                self.log.debug(self._players[player_id]["items"])
                break
        self.save_state()

    def get_items(self, name: str):
        """Returns items for player"""

        player_id = self.get_player_id_by_name(name)
        self.log.info(f"Getting items for {name}")

        return self._players[player_id]["items"]

    def convert_to_message(self, items: dict):
        """
        Converts items to message

        :param items: Dictionary of items
        :return: Message to send
        """

        message = ""
        if len(items) == 0:
            return "No items"
        for item in items:
            message += f"```{item['name']}: {item['quantity']}```\n"
        self.log.debug(f"Returning: {message}")
        return message

    def damage(self, name: str, damage: int):
        """Applies damage to player"""

        player_id = self.get_player_id_by_name(name)
        self.log.info(f"Applying {damage} to {name}")

        self._players[player_id]["hp"] -= damage
        self.save_state()

    def get_hp(self, name: str):
        """Returns HP of player"""

        player_id = self.get_player_id_by_name(name)
        self.log.info(f"Getting HP of {name}")

        return self._players[player_id]["hp"]

    def heal(self, name: str, heal: int):
        """Heals player"""

        player_id = self.get_player_id_by_name(name)
        self.log.info(f"Healing {heal} to {name}")

        self._players[player_id]["hp"] += heal
        self.save_state()
