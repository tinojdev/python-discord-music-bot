import logging
from pathlib import Path
from typing import cast

import discord

from src.models.track import Track
from asyncio import run
from src.downloader import Downloader
from src.temp_handler import TempHandler
from src.music_player_store import MusicPlayerStore

FFMPEG_OPTIONS = {
    'options': '-vn',
}

logger = logging.getLogger(__name__)


class MusicPlayer:
    _queue: list[Track] = []
    _is_started = False
    _now_playing: Track = None
    is_looping = False

    def __init__(self, guild_id, voice_client: discord.VoiceClient):
        self.guild_id = guild_id
        self.voice_client = voice_client

    async def play(self, track: Track):
        self._queue.append(track)
        if not self._is_started:
            self._is_started = True
            await self._play_next()

    async def skip(self):
        self.voice_client._player.after = None
        await self._clean_and_play_next(self._now_playing)

    def loop(self):
        self.is_looping = not self.is_looping

    def seconds_left_in_current_track(self):
        source: MusicSource = cast(MusicSource, self.voice_client.source)
        return self._now_playing.duration_seconds - source.time_played_in_seconds

    def total_length_seconds(self):
        left_in_current = self.seconds_left_in_current_track()
        return sum([track.duration_seconds for track in self._queue], left_in_current)

    def get_queue(self):
        return self._queue

    def queue_length(self):
        return len(self._queue)

    def get_now_playing(self):
        return self._now_playing

    async def _handle_error(self, error, track_to_clean: Track):
        logger.error(f"Error while playing track: {track_to_clean.title}")
        logger.error(error)
        await self._clean_and_play_next(track_to_clean)

    async def _clean_and_play_next(self, track_to_clean: Track):
        TempHandler.add_file_to_delete(track_to_clean.filename)
        if self.is_looping:
            self._queue.insert(0, track_to_clean)
        await self._play_next()

    async def _play_next(self):
        if len(self._queue) == 0:
            self._is_started = False
            self.voice_client.stop()
            await self.voice_client.disconnect(force=True)
            MusicPlayerStore.remove_music_player(self.guild_id)
            return

        track = self._queue.pop(0)
        if not track.is_downloaded():
            track = await Downloader.download(track.webpage_url)
        self._now_playing = track

        source = MusicSource(Path(TempHandler.get_temp_dir()) / track.filename)

        if self.voice_client.is_playing():
            self.voice_client.stop()

        self.voice_client.play(source,
                               after=lambda e: run(self._handle_error(e, track)) if e
                               else run(self._clean_and_play_next(track)))
        logger.info(f"Playing: {track.title}")


class MusicSource(discord.PCMVolumeTransformer):
    def __init__(self, filename, *, volume=0.5):
        super().__init__(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), volume=volume)
        self.time_played_in_seconds = 0.0

    def read(self):
        self.time_played_in_seconds += 0.02
        return super().read()


class QueueEmptyError(Exception):
    pass
