from discord import Embed
from music_player_store import MusicPlayerStore


def seconds_to_string(seconds: float):
    """Converts a seconds float to a string in the format of hh:mm:ss"""

    seconds = int(seconds)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if hours == 0:
        return f"{minutes:02d}:{seconds:02d}"
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


async def now_playing(ctx):
    music_player = MusicPlayerStore.get_music_player(ctx.guild.id)
    if music_player is None:
        return await ctx.send("No music is playing!")
    song = music_player.get_now_playing()

    if song is None:
        return await ctx.send("No music is playing!")
    description = f'[**{song.title}**]({song.webpage_url}) \nLooping: {"✅" if music_player.is_looping else "❌"}'

    embed = Embed(title="Now playing:", color=15198183, description=description)
    if song.thumbnail_url is not None:
        embed = embed.set_thumbnail(url=song.thumbnail_url)

    total_length = song.duration_seconds
    time_played = total_length - music_player.seconds_left_in_current_track()
    percentage = time_played / total_length
    progress = round(percentage * 20)
    empty_progress = 20 - progress
    progress_text = "▇" * progress
    empty_progress_text = "—" * empty_progress
    percentage_text = str(round(percentage * 100)) + "%"
    progress_bar = f"[{progress_text}{empty_progress_text}] {percentage_text}"

    embed.add_field(
        name=f"Time played {seconds_to_string(time_played)} / {seconds_to_string(total_length)}",
        value=progress_bar,
    )
    await ctx.send(embed=embed)
