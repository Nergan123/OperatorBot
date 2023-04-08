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
    @commands.has_role("DM")
    async def set_location(self, ctx: Context, location_name: str) -> None:
        """Sets location"""

        try:
            answer = self.state.get_location_service().set_location(location_name)
            image = self.state.get_location_service().get_image()
            await ctx.send(answer)
            await ctx.send(file=image)
            guild = self.state.get_guild()
            url = self.state.get_location_service().get_music(False)
            if guild:
                self.state.set_playing(True)
                vol = self.state.get_volume()
                self.state.get_sound_service().play_music(guild, url, vol)

        except KeyError:
            await ctx.send("Location not found")

    @set_location.error
    async def help_error(self, ctx: Context, error):
        """Returns an error"""

        await ctx.send(str(error).replace("'", ""))
