from dataclasses import dataclass


@dataclass
class Track:
    name: str
    album: str
    artists: list[str]
    uri: str | None = None
