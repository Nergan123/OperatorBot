import random

from discord.ext import commands
from discord.ext.commands import Context
from discord.utils import get

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
    async def end_interaction(self, ctx: Context):
        """Ends current interaction"""

        try:
            self.state.get_npc_service().end_interaction()
            if self.state.get_battle():
                self.state.set_battle(False)
                guild = self.state.bot.get_guild(self.state.get_guild())
                voice = get(self.state.bot.voice_clients, guild=guild)
                url = self.state.get_location_service().get_music(self.state.get_battle())
                self.state.get_sound_service().pause_music(voice)
                self.state.get_sound_service().play_music(
                    self.state.get_guild(),
                    url,
                    self.state.get_volume()
                )
        except KeyError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name="battle", help="Starts a battle")
    @commands.has_role("DM")
    async def battle(self, ctx: Context):
        """Starts a battle"""

        if self.state.get_npc_service().interaction is None:
            raise KeyError("No ongoing interactions")

        self.state.set_battle(True)

        guild = self.state.bot.get_guild(self.state.get_guild())
        voice = get(self.state.bot.voice_clients, guild=guild)
        url = self.state.get_location_service().get_music(self.state.get_battle())
        self.state.get_sound_service().pause_music(voice)
        self.state.get_sound_service().play_music(
            self.state.get_guild(),
            url,
            self.state.get_volume()
        )

        self.state.get_npc_service().set_initiative(True)
        players = self.state.get_player_service().get_players()
        role = get(ctx.guild.roles, name="DM")
        initiatives = []
        names = []

        # pylint: disable = cell-var-from-loop
        for player in players:
            await ctx.send(f'Roll the initiative **{player["name"]}**')
            await self.state.bot.wait_for(
                "message",
                check=lambda x: (
                    (x.author.id == player["id"]) or (role in x.author.roles)
                )
                and x.content == "!roll 1d20",
                timeout=None,
            )

            initiative = random.randint(1, 20)
            await ctx.send(f"**{player['name']}** rolls: {initiative} + {player['initiative']}")
            initiative += player["initiative"]
            initiatives.append(initiative)
            names.append(player["name"])

        npc_name = self.state.get_npc_service().get_name()
        await ctx.send(f"Roll the initiative **{npc_name}**")
        await self.state.bot.wait_for(
            "message",
            check=lambda x: (role in x.author.roles)
            and x.content == "!roll 1d20",
            timeout=None,
        )

        initiative = random.randint(1, 20)
        await ctx.send(f"**{npc_name}** rolls: {initiative}")
        initiatives.append(initiative)
        names.append(npc_name)

        message = self.state.get_npc_service().set_queue(initiatives, names)

        await ctx.send(message)
        name = self.state.get_npc_service().get_turn()
        self.state.get_npc_service().set_initiative(False)
        await ctx.send(f"Your turn **{name}**")

    @commands.command(name="turn", help="Switches to next turn in the battle")
    @commands.has_role("DM")
    async def turn(self, ctx):
        """Switches to next turn"""

        self.state.get_npc_service().next_turn()
        name = self.state.get_npc_service().get_turn()

        await ctx.send(f"Your turn **{name}**")

    @interaction.error
    @end_interaction.error
    @battle.error
    @turn.error
    async def help_error(self, ctx: Context, error):
        """Returns an error"""

        self.log.error(error)
        await ctx.send(str(error).replace("'", ""))
