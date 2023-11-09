from src.music_player_store import MusicPlayerStore


MAX_PRINTABLE_QUEUE = 20


async def queue(ctx):
    music_player = MusicPlayerStore.get_music_player(ctx.guild.id)
    if music_player is None:
        return await ctx.send("No music is playing!")

    queue = music_player.get_queue()

    if len(queue) == 0:
        return await ctx.send("No more tracks in queue.")

    printable_queue = queue
    if len(queue) > 20:
        printable_queue = queue[:MAX_PRINTABLE_QUEUE]

    track_str = ""
    for i, track in enumerate(printable_queue):
        track_str += f"{i + 1}. {track.title}\n"

    await ctx.send(f"Total of {len(queue)} tracks in queue:\n{track_str}")
