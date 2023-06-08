from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from vehicle_counter.app.server.models.history_registry import HistoryRegistrySchema


class CameraSchema(BaseModel):
    name: str = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    location: str = Field(...)

    measurements: List[HistoryRegistrySchema]


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
