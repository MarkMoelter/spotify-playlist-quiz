from pydantic import BaseModel, computed_field


class Track(BaseModel):
    name: str
    album: str
    artists: list[str]
    uri: str
    # None means Spotify didn't provide a preview for this track/market
    preview_url: str | None = None

    @computed_field()
    @property
    def is_single(self) -> bool:
        return self.name == self.album
