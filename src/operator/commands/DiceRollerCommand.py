import discord
from discord.ext import commands
from discord.ext.commands import Context

from src.operator.helpers.BaseClass import BaseClass
from src.operator.services.State import State


class DiceRollerCommand(BaseClass, commands.Cog, name="Dice rolls"):
    """Rolling dices"""

    def __init__(self, state: State):
        BaseClass.__init__(self, "dice_rolls")
        self.state = state
        self.log.info("Loaded")

    @commands.command(name="roll", help="Rolls the dices. Example: !roll 3d6")
    async def roll(self, ctx: Context, message: str) -> None:
        """Rolls the dices"""

        try:
            rolls, percent = self.state.get_dice_rolls().roll(message)
            if not self.state.get_battle():
                message = self.state.get_commentator().get_comment(
                    "dice_roll",
                    name=ctx.message.author.display_name,
                    percent=percent,
                    rolls=rolls,
                )
            else:
                role = discord.utils.get(ctx.guild.roles, name="DM")
                if role in ctx.message.author.roles:
                    player_name = self.state.get_npc_service().get_turn()
                else:
                    player_name = ctx.message.author.display_name

                message = self.state.get_commentator().get_comment(
                    "dice_roll",
                    name=player_name,
                    percent=percent,
                    rolls=rolls,
                )

            if not self.state.get_npc_service().get_initiative():
                message_disc = await ctx.send(message)
                self.state.get_sanity_service().register_entity(
                    message_disc.id,
                    message,
                    f"{ctx.channel.id}"
                )

        except ValueError as e:
            await ctx.send(str(e))

        except ZeroDivisionError:
            await ctx.send("Both values should be greater than 0")
