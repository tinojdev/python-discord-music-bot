from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.music_player import MusicPlayer


class MusicPlayerStore:
    _music_players: dict[str, "MusicPlayer"] = {}

    @classmethod
    def get_music_player(cls, guild_id):
        return cls._music_players.get(guild_id, None)

    @classmethod
    def remove_music_player(cls, guild_id):
        cls._music_players.pop(guild_id, None)

    @classmethod
    def add_music_player(cls, guild_id, music_player: "MusicPlayer"):
        cls._music_players[guild_id] = music_player
