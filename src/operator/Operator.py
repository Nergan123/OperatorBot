import discord
from discord.ext import commands

from src.operator.commands.DiceRollerCommand import DiceRollerCommand
from src.operator.commands.LocationCommand import LocationCommand
from src.operator.commands.NpcCommand import NpcCommand
from src.operator.commands.PlayerCommand import PlayerCommand
from src.operator.commands.SanityCommand import SanityCommand
from src.operator.commands.SoundCommand import SoundCommand
from src.operator.helpers.BaseClass import BaseClass
from src.operator.services.State import State


class Operator(BaseClass, commands.Bot):
    """Operator main class"""

    def __init__(self, command_prefix):
        BaseClass.__init__(self, "operator")
        intents = discord.Intents.default()
        intents.message_content = True
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)

        self.state = State(self)
        self.dice_roller = DiceRollerCommand(self.state)
        self.players = PlayerCommand(self.state)
        self.location = LocationCommand(self.state)
        self.sound = SoundCommand(self.state)
        self.npc = NpcCommand(self.state)
        self.sanity = SanityCommand(self.state)

    async def on_ready(self) -> None:
        """Log message when bot is running"""

        await self.add_cog(self.dice_roller)
        await self.add_cog(self.players)
        await self.add_cog(self.location)
        await self.add_cog(self.sound)
        await self.add_cog(self.npc)
        await self.add_cog(self.sanity)
        await self.sanity.on_load()
        await self.sound.on_load()
        print(f"{self.user.name} connected to server")
        self.log.info(f"{self.user.name} connected to server")
