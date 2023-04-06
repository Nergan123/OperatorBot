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

        try:
            self.state.get_player_service().add_player(ctx, message)
            self.log.info("Added new player")

            await ctx.send("Player registered")
        except KeyError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name="remove_player", help="Removes player from a campaign")
    async def remove_player(self, ctx: Context, name: str):
        """Removes player from current campaign"""

        try:
            player_id = self.state.get_player_service().get_player_id_by_name(name)
            self.state.get_player_service().remove_player(player_id)
            await ctx.send(f"Removed: {name}")
        except ValueError as error:
            await ctx.send(str(error).replace("'", ""))
