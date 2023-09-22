from typing import Optional
from dataclasses import dataclass


@dataclass
class Track:
    title: str
    thumbnail_url: Optional[str]
    webpage_url: str
    uploader: str
    duration_seconds: int
    filename: Optional[str]
    added_by: Optional[str]

    def is_downloaded(self) -> bool:
        return self.filename is not None
