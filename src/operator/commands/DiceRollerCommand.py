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
            message = self.state.get_commentator().get_comment(
                "dice_roll",
                name=ctx.message.author.display_name,
                percent=percent,
                rolls=rolls,
            )

            await ctx.reply(message)

        except ValueError as e:
            await ctx.reply(str(e))

        except ZeroDivisionError:
            await ctx.reply("Both values should be greater than 0")
