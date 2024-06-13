from pydantic import BaseModel, computed_field


class Track(BaseModel):
    name: str
    album: str
    artists: list[str]
    uri: str = None

    @computed_field()
    @property
    def is_single(self) -> bool:
        return self.name == self.album
