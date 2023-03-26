import yt_dlp
import os

from pathlib import Path
from src.models.track import Track
from src.temp_handler import TempHandler

YTDL_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': f'{TempHandler.get_temp_dir()}/downloaded.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = yt_dlp.YoutubeDL(
    YTDL_FORMAT_OPTIONS
)


class Downloader:

    @classmethod
    async def get_track_info(cls, url) -> Track:
        data = ytdl.extract_info(url, download=False)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        return parse_dict_to_track(data)

    @classmethod
    async def download(cls, url) -> Track:
        data = ytdl.extract_info(url, download=True)
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = ytdl.prepare_filename(data)
        # go from ./temp/xxx to xxx
        filename = Path(filename).name
        random_filename = os.urandom(24).hex()
        temp_dir = TempHandler.get_temp_dir()

        os.rename(os.path.join(temp_dir, filename), os.path.join(temp_dir, random_filename))

        filename = random_filename
        return parse_dict_to_track(data, filename)


def parse_dict_to_track(data, filename=None) -> Track:
    return Track(
        title=data.get("title"),
        thumbnail_url=data.get("thumbnail"),
        webpage_url=data.get("webpage_url"),
        uploader=data.get("uploader"),
        filename=filename,
        duration_seconds=data.get("duration"),
        added_by=None
    )
