from __future__ import annotations

import yt_dlp
import os
import logging

from pathlib import Path
from urllib.parse import urlparse
from models.track import Track
from temp_handler import TempHandler

YTDL_FORMAT_OPTIONS = {
    "format": "bestaudio/best",
    "outtmpl": f"{TempHandler.get_temp_dir()}/downloaded",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

logger = logging.getLogger(__name__)

ytdl = yt_dlp.YoutubeDL(YTDL_FORMAT_OPTIONS)


class Downloader:
    @classmethod
    async def get_track_info(cls, url) -> Track:
        data = ytdl.extract_info(url, download=False)
        return parse_dict_to_track(data)

    @classmethod
    async def download(cls, url) -> Track:
        data = ytdl.extract_info(url, download=True)
        filename = ytdl.prepare_filename(data)
        # go from ./temp/xxx to xxx
        filename = Path(filename).name
        random_filename = os.urandom(24).hex()
        temp_dir = TempHandler.get_temp_dir()

        os.rename(
            os.path.join(temp_dir, filename), os.path.join(temp_dir, random_filename)
        )

        filename = random_filename
        return parse_dict_to_track(data, filename)

    YTDL_PLAYLIST_OPTIONS = {
        "extract_flat": "in_playlist",
        "skip_download": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
    }

    @classmethod
    async def get_playlist_songs(cls, url) -> list[Track]:
        if not is_valid_youtube_playlist_url(url):
            raise InvalidUrlError("Invalid playlist url")

        with yt_dlp.YoutubeDL(cls.YTDL_PLAYLIST_OPTIONS) as ydl:
            try:
                data = ydl.extract_info(url)
            except Exception as e:
                logger.error("Error while getting playlist songs")
                logger.error(e)
                raise NotFoundError("Playlist not found")

            if data is None:
                raise NotFoundError("Playlist not found")

            print(data)
            if "entries" in data:
                songs = [
                    parse_playlist_dict_to_track(song)
                    for song in data["entries"]
                    if song is not None
                ]
                return songs
            else:
                raise NotFoundError("Playlist not found")


def parse_playlist_dict_to_track(data) -> Track:
    thumbnails = data.get("thumbnails")
    thumbnail_url: str | None = thumbnails[0]["url"] if thumbnails else None

    return Track(
        title=data.get("title"),
        thumbnail_url=thumbnail_url,
        webpage_url=data.get("url"),
        uploader=data.get("uploader"),
        filename=None,
        added_by=None,
        duration_seconds=data.get("duration"),
    )


def parse_dict_to_track(data, filename=None) -> Track:
    return Track(
        title=data.get("title"),
        thumbnail_url=data.get("thumbnail"),
        webpage_url=data.get("webpage_url"),
        uploader=data.get("uploader"),
        filename=filename,
        duration_seconds=data.get("duration"),
        added_by=None,
    )


def is_valid_youtube_playlist_url(url) -> bool:
    res = urlparse(url)
    if res.scheme != "https":
        return False
    if res.netloc != "www.youtube.com":
        return False
    if "&list=" not in res.query:
        return False
    return True


class NotFoundError(Exception):
    pass


class InvalidUrlError(Exception):
    pass
