from anythingwebapp.schemas.base import BaseModel


class File(BaseModel):
    data: bytes
    mime_type: str
