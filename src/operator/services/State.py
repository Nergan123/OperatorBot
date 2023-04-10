from src.operator.helpers.BaseClass import BaseClass
from src.operator.services.commentator.CommentatorService import CommentatorService
from src.operator.services.dice_rolls.DiceRollerService import DiceRollerService
from src.operator.services.location.LocationService import LocationService
from src.operator.services.npc.NpcService import NpcService
from src.operator.services.player.PlayerService import PlayerService
from src.operator.services.sound.SoundService import SoundService


class State(BaseClass):
    """Campaign state"""

    SERIALIZABLE_FIELDS = [
        "_voice_channel_id",
        "_guild_id",
        "_playing",
        "_volume",
        "_battle"
    ]

    def __init__(self, bot):
        super().__init__("campaign_state")
        self._dice_rolls = DiceRollerService()
        self._commentator = CommentatorService()
        self._players = PlayerService()
        self._location_service = LocationService()
        self._sound_service = SoundService(bot)
        self._npc = NpcService()

        self._voice_channel_id = None
        self._guild_id = None
        self._voice_channel = None
        self._playing = False
        self._volume = 1
        self._battle = False
        self.bot = bot
        self.load_state()

    def get_dice_rolls(self):
        """Returns dice roller service"""

        return self._dice_rolls

    def get_commentator(self):
        """Returns a commentator service"""

        return self._commentator

    def get_player_service(self):
        """Returns player service"""

        return self._players

    def get_location_service(self):
        """Returns location service"""

        return self._location_service

    def get_sound_service(self):
        """Returns sound_service"""

        return self._sound_service

    def set_voice(self, channel_id: int | None, channel):
        """Records voice channel id"""

        self._voice_channel_id = channel_id
        self._voice_channel = channel
        self.save_state()
        self.log.info(f"Voice channel set to: {channel_id}")

    def get_voice_id(self) -> int:
        """Returns voice channel id"""

        return self._voice_channel_id

    def get_voice_channel(self):
        """returns voice channel"""

        return self._voice_channel

    def set_guild_id(self, guild_id: int):
        """Sets guild_id"""

        self._guild_id = guild_id
        self.log.info(f"Guild id set: {guild_id}")
        self.save_state()

    def get_guild(self):
        """Returns guild_id"""

        return self._guild_id

    def set_playing(self, playing: bool):
        """Sets status of music"""

        self._playing = playing
        self.save_state()

    def get_playing(self):
        """Returns status of music"""

        return self._playing

    def set_volume(self, vol: float):
        """Stores volume data"""

        self._volume = vol
        self.save_state()

    def get_volume(self):
        """returns volume val"""

        return self._volume

    def get_npc_service(self):
        """Returns npc service"""

        return self._npc

    def set_battle(self, val: bool):
        """Sets battle status"""

        self._battle = val
        self.save_state()

    def get_battle(self):
        """Returns battle status"""

        return self._battle
