import random

from discord.ext import commands, tasks
from discord.ext.commands import Context

from src.operator.helpers.BaseClass import BaseClass
from src.operator.services.State import State


class SanityCommand(BaseClass, commands.Cog, name="Internal"):
    """DM mechanics"""

    def __init__(self, state: State):
        BaseClass.__init__(self, "sanity_commands")
        self.state = state
        self.log.info("Loaded")

    @commands.command(name="sanity", help="")
    @commands.has_role("DM")
    async def sanity(self, ctx: Context, level: int):
        """Changes everything"""

        await ctx.message.delete()
        self.log.info("Message deleted")
        self.state.get_sanity_service().set_level(level)

    async def on_load(self):
        """Initializing"""

        # pylint: disable = no-member
        self.log.info("Launching services")
        self.change_discord.start()

    @tasks.loop(seconds=1)
    async def change_discord(self):
        """Changes an appearance"""

        level = self.state.get_sanity_service().get_level()
        if random.randint(0, 100) <= level:
            self.log.info("Changing")
