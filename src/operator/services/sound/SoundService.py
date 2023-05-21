from yt_dlp import YoutubeDL

from discord import FFmpegPCMAudio
from discord import PCMVolumeTransformer
from discord.utils import get

from src.operator.helpers.BaseClass import BaseClass


class SoundService(BaseClass):
    """Service responsible for sound control"""

    def __init__(self, bot):
        super().__init__("sound_service")
        self.bot = bot
        self.log.info("Loaded")

    def play_music(self, guild_id: int, url: str, volume: float):
        """Plays the music"""

        ydl_options = {"format": "bestaudio", "noplaylist": "True"}
        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn",
        }

        guild = self.bot.get_guild(guild_id)
        self.log.info(f"Got guild: {guild}")
        voice = get(self.bot.voice_clients, guild=guild)

        if voice:
            if not voice.is_playing():
                with YoutubeDL(ydl_options) as ydl:
                    info = ydl.extract_info(url, download=False)
                url_yt = info["url"]
                self.log.info(f"Playing: {url}")
                voice.play(FFmpegPCMAudio(url_yt, **ffmpeg_options))
                voice.source = PCMVolumeTransformer(voice.source, volume=volume)
                voice.is_playing()
            else:
                return

    def pause_music(self, voice):
        """Pauses current music"""

        if voice:
            if voice.is_playing():
                self.log.info("Pausing")
                voice.pause()
            else:
                raise AttributeError("Not playing")

    def resume_music(self, voice):
        """resumes current music"""

        if voice.is_paused():
            self.log.info("Resuming")
            voice.resume()
            return

        raise AttributeError("Music not paused")
