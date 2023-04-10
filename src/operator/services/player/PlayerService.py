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

        if ctx.message.author.id in self._players:
            raise KeyError("Player already exists")

        self._players[ctx.message.author.id] = asdict(PlayerData(ctx, name))
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
