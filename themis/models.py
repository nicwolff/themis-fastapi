from datetime import datetime
from pydantic import BaseModel, Json
from uuid import UUID


class ThemeBase(BaseModel):
    resource_id: UUID = None
    resource_type: str = None
    slug: str = None
    theme: Json = None


class ThemePatch(ThemeBase):
    pass


class ThemePost(ThemeBase):
    resource_id: UUID
    resource_type: str
    slug: str
    theme: Json


class ThemePut(ThemePost):
    pass


class ThemeRecord(ThemePost):
    ID: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
