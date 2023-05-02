import random

from discord.ext import commands, tasks
from discord.ext.commands import Context
from discord.utils import get

from src.operator.helpers.BaseClass import BaseClass
from src.operator.services.State import State


class SanityCommand(BaseClass, commands.Cog, name="Internal"):
    """DM mechanics"""

    def __init__(self, state: State):
        BaseClass.__init__(self, "sanity_commands")
        self.state = state
        self.log.info("Loaded")

    @commands.command(name="level", help="")
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

    @commands.command(name="restore", help="")
    @commands.has_role("DM")
    async def restore_messages(self, ctx: Context):
        """Restores everything"""

        self.log.info("Restoring everything")
        await ctx.message.delete()
        await self.state.get_sanity_service().restore(self.state.bot)
        self.state.get_sanity_service().set_level(0)

    @tasks.loop(seconds=3)
    async def change_discord(self):
        """Changes an appearance"""

        level = self.state.get_sanity_service().get_level()

        level = min(level, 90)

        type_of_actions = 0
        if level <= 30:
            type_of_actions = random.randint(0, 1)
        elif 30 < level <= 60:
            type_of_actions = random.randint(0, 2)
        elif 60 < level <= 80:
            type_of_actions = random.randint(0, 3)
        elif 80 < level:
            type_of_actions = random.randint(0, 4)

        if random.randint(0, 100) < level:
            if type_of_actions == 0:
                await self.state.get_sanity_service().change_entity(level, self.state.bot)

            elif type_of_actions == 1:
                await self.state.get_sanity_service().restore_random(self.state.bot)

            elif type_of_actions == 2:
                if random.randint(0, 100) < 10:
                    await self.change_sound()

            elif type_of_actions == 3:
                timer = random.randint(1, 3)
                img, channel = self.state.get_sanity_service().get_image(self.state.bot)
                await channel.send(file=img, delete_after=timer)

            elif type_of_actions == 4:
                if random.randint(0, 100) < 30:
                    await self.send_messages()

    async def change_sound(self):
        """Changes sound to random music sfx"""

        guild = self.state.get_guild()
        url = self.state.get_sanity_service().get_url()
        if guild:
            if not self.state.get_playing():
                self.state.set_playing(True)
                vol = self.state.get_volume()
                self.state.get_sound_service().play_music(guild, url, vol)
            else:
                voice = get(
                    self.state.bot.voice_clients,
                    guild=self.state.bot.get_guild(self.state.get_guild())
                )
                self.state.get_sound_service().pause_music(voice)
                vol = self.state.get_volume()
                self.state.get_sound_service().play_music(guild, url, vol)
        return

    async def send_messages(self):
        """Sends random messages to players"""

        players = self.state.get_player_service().get_players()
        for player in players:
            self.log.info(f"Sending message to {player['name']}")
            message = self.state.get_sanity_service().get_message(player["role"])
            user = await self.state.bot.fetch_user(player["id"])
            await user.send(message)
