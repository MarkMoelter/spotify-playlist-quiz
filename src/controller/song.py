from dataclasses import dataclass


@dataclass
class Song:
    name: str
    album: str
    artists: list[str]
    uri: str = None
