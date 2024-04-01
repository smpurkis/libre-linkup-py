from enum import Enum
from pydantic import BaseModel, HttpUrl


class LibreLinkUpUrl(Enum):
    GLOBAL: HttpUrl = HttpUrl("https://api.libreview.io")
    EU: HttpUrl = HttpUrl("https://api-eu2.libreview.io")


class ReadingSource(Enum):
    LOGBOOK: str = "logbook"
    GRAPH: str = "graph"
    LATEST_READING: str = "latest_reading"


class GlucoseSensorReading(BaseModel):
    unix_timestamp: float
    value: float
    value_in_mg_per_dl: float
    source: ReadingSource


class Connection(BaseModel):
    patient_id: str
    first_name: str
    last_name: str
