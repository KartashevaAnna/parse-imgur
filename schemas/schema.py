from pydantic import BaseModel, computed_field


class Album(BaseModel):
    id: str
    title: str

    @computed_field
    @property
    def link(cls) -> str:
        return f"https://api.imgur.com/3/album/{cls.id}"


class Image(BaseModel):
    link: str
