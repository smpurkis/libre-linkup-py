from enum import Enum
from pydantic import BaseModel, HttpUrl


class LibreLinkUpUrl(Enum):
    GLOBAL: HttpUrl = HttpUrl("https://api.libreview.io")
    EU: HttpUrl = HttpUrl("https://api-eu2.libreview.io")


class GlucoseSensorReading(BaseModel):
    unix_timestamp: float
    value: float
    value_in_mg_per_dl: float
    low_at_the_time: bool
    high_at_the_time: bool


class Connection(BaseModel):
    patient_id: str
    first_name: str
    last_name: str
