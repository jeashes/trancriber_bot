from pydantic import BaseModel


class Voice(BaseModel):
    voice: str


class VideoNote(BaseModel):
    video_note: str
