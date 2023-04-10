from discord.ext import commands
from discord.ext.commands import Context

from src.operator.helpers.BaseClass import BaseClass
from src.operator.services.State import State


class NpcCommand(BaseClass, commands.Cog, name="NPC interactions"):
    """Commands to interact with NPCs"""

    def __init__(self, state: State):
        BaseClass.__init__(self, "npc_command")
        self.state = state
        self.log.info("Loaded")

    @commands.command(name="interaction", help="Activates interaction with an NPC")
    @commands.has_role("DM")
    async def interaction(self, ctx: Context, name: str):
        """Starts an interaction with an NPC"""

        try:
            npc = self.state.get_location_service().get_npc(name)
            self.log.info(f"Receiving: {npc}")
            name = self.state.get_npc_service().load_npc(npc)
            image = self.state.get_npc_service().get_image()

            await ctx.send(f"Detecting {name}")
            await ctx.send(file=image)
        except KeyError as error:
            self.log.error(error)
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name="end_interaction", help="Ends ongoing interaction")
    @commands.has_role("DM")
    async def end_interaction(self, ctx):
        """Ends current interaction"""

        try:
            self.state.get_npc_service().end_interaction()
        except KeyError as error:
            await ctx.send(str(error).replace("'", ""))

    @interaction.error
    @end_interaction.error
    async def help_error(self, ctx: Context, error):
        """Returns an error"""

        await ctx.send(str(error).replace("'", ""))
