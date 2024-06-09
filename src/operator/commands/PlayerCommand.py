from discord.ext import commands
from discord.ext.commands import Context

from src.operator.helpers.BaseClass import BaseClass
from src.operator.services.State import State


class PlayerCommand(BaseClass, commands.Cog, name="Players handling"):
    """Maintains players"""

    def __init__(self, state: State):
        BaseClass.__init__(self, "player_command")
        self.state = state
        self.log.info("Loaded")

    @commands.command(name="add_player", help="Adds player to the current campaign")
    async def add_player(self, ctx: Context, message: str):
        """Adds player to the campaign"""

        try:
            self.state.get_player_service().add_player(ctx, message)
            self.log.info("Added new player")

            await ctx.send("Player registered")
        except KeyError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name="remove_player", help="Removes player from a campaign")
    async def remove_player(self, ctx: Context, name: str):
        """Removes player from current campaign"""

        try:
            player_id = self.state.get_player_service().get_player_id_by_name(name)
            self.state.get_player_service().remove_player(player_id)
            await ctx.send(f"Removed: {name}")
        except ValueError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name="set_initiative", help="Sets an initiative modifier for player")
    async def set_initiative(self, ctx: Context, name: str, val: int):
        """Sets an initiative modifier for a player"""

        try:
            self.state.get_player_service().set_initiative(name, int(val))
            await ctx.send(f"Set initiative modifier for {name}")
        except ValueError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name="add_item", help="Adds an item to player")
    @commands.has_role("DM")
    async def add_item(self, ctx: Context, name: str, item: str, quantity: int):
        """Adds an item to player"""

        try:
            self.state.get_player_service().add_item(name, item, quantity)
            await ctx.send(f"Added item to {name}")
        except ValueError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name="edit_item", help="edit an item in player")
    @commands.has_role("DM")
    async def edit_item(self, ctx: Context, name: str, item: str, quantity: int):
        """Edits an item in player"""

        try:
            self.state.get_player_service().edit_item(name, item, quantity)
            await ctx.send(f"Edited item in {name}")
        except ValueError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name="remove_item", help="Removes an item from player")
    @commands.has_role("DM")
    async def remove_item(self, ctx: Context, name: str, item: str):
        """Removes an item from player"""

        try:
            self.state.get_player_service().remove_item(name, item)
            await ctx.send(f"Removed item from {name}")
        except ValueError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name="show_items", help="Shows items of a player")
    async def show_items(self, ctx: Context, name: str = None):
        """Shows items of a player"""

        if name is None:
            player_id = ctx.message.author.id
            name = self.state.get_player_service().get_player_by_id(player_id)["name"]

        try:
            items = self.state.get_player_service().get_items(name)
            message = self.state.get_player_service().convert_to_message(items)
            await ctx.send(message)
        except ValueError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name="show_player", help="Shows player data")
    async def show_player(self, ctx: Context, name: str = None):
        """Shows player data"""

        if name is None:
            player_id = ctx.message.author.id
            name = self.state.get_player_service().get_player_by_id(str(player_id))["name"]

        try:
            player = self.state.get_player_service().get_player_by_name(name)
            message = f"**Name**: {player['name']}\n\n"
            message += f"**HP**: {player['hp']}\n"
            message += f"**Initiative**: {player['initiative']}\n"
            message += f"**Role**: {player['role']}\n"
            items = self.state.get_player_service().get_items(name)
            items = self.state.get_player_service().convert_to_message(items)
            message += f"**Items**: \n{items}\n"
            await ctx.send(message)
        except ValueError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name="damage", help="Deals damage to a player")
    @commands.has_role("DM")
    async def damage(self, ctx: Context, name: str, damage: int):
        """Deals damage to a player"""

        try:
            self.state.get_player_service().damage(name, damage)
            message = f"Dealt {damage} damage to {name}"
            message += f"\n\n**{name}** has {self.state.get_player_service().get_hp(name)} HP left"
            await ctx.send(message)
        except ValueError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name="heal", help="Heals a player")
    @commands.has_role("DM")
    async def heal(self, ctx: Context, name: str, heal: int):
        """Heals a player"""

        try:
            self.state.get_player_service().heal(name, heal)
            message = f"Healed {heal} to {name}"
            message += f"\n\n**{name}** has {self.state.get_player_service().get_hp(name)} HP left"
            await ctx.send(message)
        except ValueError as error:
            await ctx.send(str(error).replace("'", ""))
