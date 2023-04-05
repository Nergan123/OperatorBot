from dataclasses import asdict

from discord.ext.commands import Context

from src.operator.helpers.BaseClass import BaseClass
from src.player.PlayerData import PlayerData


class PlayerService(BaseClass):
    """Class to handle players"""

    SERIALIZABLE_FIELDS = [
        "players"
    ]

    def __init__(self):
        self.players = {}
        super().__init__("player_service")

    def add_player(self, ctx: Context, name: str):
        """Adds player to list"""

        self.players[ctx.message.author.id] = asdict(PlayerData(ctx, name))
        self.save_state()
