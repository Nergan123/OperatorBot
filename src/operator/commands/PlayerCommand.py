from discord.ext import commands
from discord.ext.commands import Context

from src.operator.helpers.BaseClass import BaseClass
from src.operator.services.State import State


class PlayerCommand(BaseClass, commands.Cog, name="Players handling"):
    """Maintains players"""

    def __init__(self, state: State):
        BaseClass.__init__(self, "player_command")
        self.state = state
        self.log.info("Loaded")

    @commands.command(name="add_player", help="Adds player to the current campaign")
    async def add_player(self, ctx: Context, message: str):
        """Adds player to the campaign"""

        self.state.get_player_service().add_player(ctx, message)
        self.log.info("Added new player")

        await ctx.reply("Player registered")
