import yt_dlp
import os

from pathlib import Path
from models.track import Track
from temp_handler import TempHandler

YTDL_FORMAT_OPTIONS = {
    "format": "bestaudio/best",
    "outtmpl": f"{TempHandler.get_temp_dir()}/downloaded.%(ext)s",
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
        with yt_dlp.YoutubeDL(cls.YTDL_PLAYLIST_OPTIONS) as ydl:
            data = ydl.extract_info(url)
            if data is None:
                raise NotFoundError("Playlist not found")

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


class NotFoundError(Exception):
    pass
