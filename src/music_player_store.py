from __future__ import annotations

from typing import TYPE_CHECKING
from music_player import MusicPlayer

if TYPE_CHECKING:
    from music_player import MusicPlayer


class MusicPlayerStore:
    _music_players: dict[str, "MusicPlayer"] = {}

    @classmethod
    def get_music_player(cls, guild_id):
        return cls._music_players.get(guild_id, None)

    @classmethod
    def get_or_create_music_player(cls, guild_id, voice_client):
        music_player = cls.get_music_player(guild_id)
        if music_player is None:
            music_player = MusicPlayer(guild_id, voice_client)
            cls.add_music_player(guild_id, music_player)
        return music_player

    @classmethod
    def remove_music_player(cls, guild_id):
        cls._music_players.pop(guild_id, None)

    @classmethod
    def add_music_player(cls, guild_id, music_player: "MusicPlayer"):
        cls._music_players[guild_id] = music_player
