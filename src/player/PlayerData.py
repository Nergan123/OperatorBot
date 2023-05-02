from dataclasses import dataclass

import discord
from discord.ext.commands import Context

from src.operator.helpers.logging.LoggerBase import LoggingHandler


@dataclass
class PlayerData(LoggingHandler):
    """Stores player data"""

    name: str
    id: int
    state: int
    initiative: int
    role: str

    def __init__(self, ctx: Context, message: str):
        super().__init__()

        roles = [
            "DM",
            "IT_specialist",
            "Security",
            "Engineer",
            "Medic"
        ]

        for role in roles:
            role_discord = discord.utils.get(ctx.guild.roles, name=role)
            if role_discord in ctx.message.author.roles:
                self.role = role
                break

        self.name = message.replace(" ", "")
        self.id = ctx.message.author.id
        self.state = 0
        self.initiative = 0
        self.log.info(f"Loaded character: {self.name}")
