from discord.ext import commands
from discord.ext.commands import Context

from src.operator.helpers.BaseClass import BaseClass
from src.operator.services.State import State


class LocationCommand(BaseClass, commands.Cog, name="Location setting. DM role required"):
    """Controls current location"""

    def __init__(self, state: State):
        BaseClass.__init__(self, "location_command")
        self.state = state
        self.log.info("Loaded")

    @commands.command(name="set_location", help="Sets current location")
    async def location_set(self, ctx: Context, location_name: str, *args) -> None:
        """Sets location for player"""

        try:
            for name in args:
                self.log.info(args)
                player_id = self.state.get_player_service().get_player_id_by_name(name)
                self.state.get_player_service().set_parameter(player_id, "location", location_name)
                await ctx.send(f"{name} moves to {location_name}")

        except ValueError as error:
            await ctx.send(str(error).replace("'", ""))
