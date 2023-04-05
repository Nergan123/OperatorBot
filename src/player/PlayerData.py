from dataclasses import dataclass

from discord.ext.commands import Context

from src.operator.helpers.logging.LoggerBase import LoggingHandler


@dataclass
class PlayerData(LoggingHandler):
    """Stores player data"""

    name: str
    id: int
    state: int
    location: str
    filename: str

    def __init__(self, ctx: Context, message: str):
        super().__init__()

        self.name = message.replace(" ", "")
        self.id = ctx.message.author.id
        self.state = 0
        self.location = ""
        self.log.info(f"Loaded character: {self.name}")
