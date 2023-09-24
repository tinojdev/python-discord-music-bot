import logging
from discord.ext.commands import Context
from downloader import Downloader, NotFoundError
from music_player_store import MusicPlayerStore

logger = logging.getLogger(__name__)


async def play_playlist(ctx: Context, url: str):
    if not ctx.guild:
        return
    music_player = MusicPlayerStore.get_or_create_music_player(
        ctx.guild.id, ctx.voice_client
    )
    msg = await ctx.reply("Searching for playlist...")
    try:
        songs = await Downloader.get_playlist_songs(url)
    except NotFoundError:
        await msg.edit(content="Playlist not found :(")
        if music_player.is_empty_queue():
            await music_player.disconnect()
        return
    except Exception as e:
        logger.error(e)
        await msg.edit(content="Error while trying to get playlist songs.")

        if music_player.is_empty_queue():
            await music_player.disconnect()
        return

    await msg.edit(content=f"Found {len(songs)} songs. Adding to queue...")

    async with ctx.typing():
        is_empty_queue = music_player.is_empty_queue()
        first_song = songs.pop(0)
        for song in songs:
            song.added_by = ctx.author.display_name
            await music_player.play(song)
        if is_empty_queue:
            await ctx.send(f"Now playing: {first_song.title}")
