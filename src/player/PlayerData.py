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
    hp: int
    items: list

    def __init__(self, ctx: Context, message: str):
        super().__init__()

        roles = [
            "DM",
            "Marauder",
            "Medic",
            "Sniper"
            "Engineer",
            "Scout",
        ]

        for role in roles:
            role_discord = discord.utils.get(ctx.guild.roles, name=role)
            if role_discord in ctx.message.author.roles:
                self.role = role
                break

        if self.role == "DM":
            self.hp = 9999
        elif self.role == "Marauder":
            self.hp = 15
        elif self.role == "Medic":
            self.hp = 13
        elif self.role == "Sniper":
            self.hp = 15
        elif self.role == "Engineer":
            self.hp = 14
        elif self.role == "Scout":
            self.hp = 18

        self.name = message.replace(" ", "")
        self.id = ctx.message.author.id
        self.state = 0
        self.initiative = 0
        self.items = [
            {
                "name": "ammo",
                "quantity": 15,
            },
            {
                "name": "ammo",
                "quantity": 15,
            },
        ]
        self.log.info(f"Loaded character: {self.name}")
