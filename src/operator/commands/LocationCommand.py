from discord.ext import commands

from src.operator.helpers.BaseClass import BaseClass
from src.operator.services.State import State


class LocationCommand(BaseClass, commands.Cog, name="Location setting. DM role required"):
    """Controls current location"""

    def __init__(self, state: State):
        BaseClass.__init__(self, "location_command")
        self.state = state
        self.log.info("Loaded")

    @commands.command(name="set_location", help="Sets current location")
    async def location_set(self, ctx, location_name: str, **kwargs) -> None:
        """Sets location for player"""

        raise NotImplementedError("Module not implemented yet")
