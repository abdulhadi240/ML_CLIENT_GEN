from pydantic import BaseModel



class CheckBanner(BaseModel):
    image_url: str | None = None



class HeadlineRequest(BaseModel):
    prev_headline: str


class CheckProfile(BaseModel):
    image_url: str | None = None