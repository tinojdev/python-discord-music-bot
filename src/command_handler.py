import logging

from discord.ext import commands
from discord.ext.commands import Bot
from commands.play import play
from commands.play_playlist import play_playlist
from commands.now_playing import now_playing
from commands.queue import queue

from music_player_store import MusicPlayerStore

logger = logging.getLogger(__name__)


class CommandHandler(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, url: str):
        return await play(ctx, url)

    @commands.command(aliases=["pp", "playlist"])
    async def play_playlist(self, ctx, *, url: str):
        return await play_playlist(ctx, url)

    @commands.command(aliases=["s"])
    async def skip(self, ctx):
        music_player = MusicPlayerStore.get_music_player(ctx.guild.id)
        if music_player is None:
            return await ctx.send("No music is playing.")
        if music_player.is_looping:
            music_player.loop()
        await music_player.skip()
        await ctx.send("Skipped!")

    @commands.command()
    async def shuffle(self, ctx):
        music_player = MusicPlayerStore.get_music_player(ctx.guild.id)
        if music_player is None:
            return await ctx.send("No music is playing.")
        await music_player.shuffle()

    @commands.command()
    async def loop(self, ctx):
        music_player = MusicPlayerStore.get_music_player(ctx.guild.id)
        if music_player is None:
            return await ctx.send("No music is playing.")
        if music_player.is_looping:
            await ctx.send("No longer looping the current song")
        else:
            await ctx.send("Looping the current song 🔁")
        music_player.loop()

    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        return await queue(ctx)

    @commands.command(aliases=["np"])
    async def now_playing(self, ctx):
        return await now_playing(ctx)

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        music_player = MusicPlayerStore.get_music_player(ctx.guild.id)
        if music_player is None:
            return await ctx.send("No music is playing!")
        await music_player.voice_client.disconnect()

    @play.before_invoke
    @play_playlist.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
