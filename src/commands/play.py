import logging
from discord.ext.commands import Context
from src.music_player_store import MusicPlayerStore
from src.downloader import Downloader

logger = logging.getLogger(__name__)


async def play(ctx: Context, url: str):
    if ctx.guild is None:
        return await ctx.send("This command can only be used in a server.")

    music_player = MusicPlayerStore.get_or_create_music_player(
        ctx.guild.id, ctx.voice_client
    )
    async with ctx.typing():
        try:
            if music_player.is_empty_queue():
                track = await Downloader.get_track_info(url)
            else:
                track = await Downloader.download(url)
            track.added_by = ctx.author.display_name
            await music_player.play(track)
        except Exception as e:
            logger.error(e)
            await ctx.send("Error while trying to play the song.")
            if music_player.is_empty_queue():
                await music_player.disconnect()
            return
        if not music_player.is_empty_queue():
            await ctx.send(f"Added to queue: {track.title}")
        else:
            await ctx.send(f"Now playing: {track.title}")
