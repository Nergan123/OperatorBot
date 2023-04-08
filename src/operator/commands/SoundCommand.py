from discord.ext import commands, tasks
from discord.ext.commands import Context
from discord.utils import get

from src.operator.helpers.BaseClass import BaseClass
from src.operator.services.State import State


class SoundCommand(BaseClass, commands.Cog, name="Sound control"):
    """Interacting with sound"""

    def __init__(self, state: State):
        BaseClass.__init__(self, "sound_command")
        self.state = state

    @commands.command(
        name="join_voice", help="Bot will join voice chat you're in. DM role required"
    )
    @commands.has_role("DM")
    async def join_voice(self, ctx: Context):
        """Bot joins the voice chat"""

        if not ctx.message.author.voice:
            await ctx.send(
                f"{ctx.message.author.display_name} is not connected to a voice channel"
            )
            return

        channel = ctx.message.author.voice.channel
        guild = ctx.guild.id
        self.state.set_voice(channel.id, channel)
        self.state.set_guild_id(guild)
        await channel.connect()

    @commands.command(name="leave_voice", help="Bot leaves the voice. DM role required")
    @commands.has_role("DM")
    async def leave_voice(self, ctx):
        """Command to leave the voice chat"""

        if not ctx.message.author.voice:
            await ctx.send(
                f"{ctx.message.author.display_name} is not connected to a voice channel"
            )
            return

        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            self.state.set_voice(None, None)
            self.state.set_playing(False)
        else:
            await ctx.send("I'm not in a voice chat")

    @commands.command(name="play", help="Plays the music")
    async def play(self, ctx):
        """Starts the music"""

        if not ctx.voice_client:
            await ctx.send("I'm not in a voice channel")

        if not self.state.get_playing():
            guild_id = self.state.get_guild()
            url = self.state.get_location_service().get_music(False)
            self.state.set_playing(True)
            vol = self.state.get_volume()
            self.state.get_sound_service().play_music(guild_id, url, vol)
        else:
            await ctx.send("Already playing")

    @commands.command(name='pause', help='Pauses the music.')
    async def pause(self, ctx):
        """Pauses playing music"""

        voice = get(self.state.bot.voice_clients, guild=ctx.guild)
        try:
            self.state.get_sound_service().pause_music(voice)
            self.state.set_playing(False)
        except AttributeError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name='resume', help='Resumes music.')
    async def resume(self, ctx):
        """resumes current music"""

        voice = get(self.state.bot.voice_clients, guild=ctx.guild)
        try:
            self.state.get_sound_service().resume_music(voice)
            self.state.set_playing(True)
        except AttributeError as error:
            await ctx.send(str(error).replace("'", ""))

    @commands.command(name='volume', help='Sets volume of the bot.')
    async def volume(self, ctx, vol: int):
        """Sets playing volume"""

        if ctx.voice_client:
            voice = get(self.state.bot.voice_clients, guild=ctx.guild)
            if 0 <= vol <= 100:
                new_volume = vol / 100
                voice.source.volume = new_volume
                self.state.set_volume(new_volume)
            else:
                await ctx.send('Please enter a volume between 0 and 100')

    @join_voice.error
    @leave_voice.error
    async def help_error(self, ctx: Context, error):
        """Returns an error"""

        await ctx.send(str(error).replace("'", ""))

    async def on_load(self):
        """Initializing"""

        channel_id = self.state.get_voice_id()
        channel = self.state.bot.get_channel(channel_id)
        self.state.set_voice(channel_id, channel)
        if channel:
            await channel.connect()
            self.log.info("Connected to voice")

        if self.state.get_playing():
            vol = self.state.get_volume()
            self.state.get_sound_service().play_music(
                self.state.get_guild(),
                self.state.get_location_service().get_music(False),
                vol
            )
        # pylint: disable = no-member
        await self.check_playing.start()

    @tasks.loop(seconds=5)
    async def check_playing(self):
        """Checks if song has finished"""

        guild = self.state.bot.get_guild(self.state.get_guild())

        voice = get(self.state.bot.voice_clients, guild=guild)
        if not voice.is_playing() and self.state.get_playing():
            self.state.set_playing(True)
            vol = self.state.get_volume()
            self.state.get_sound_service().play_music(
                self.state.get_guild(),
                self.state.get_location_service().get_music(False),
                vol
            )
