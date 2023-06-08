from datetime import datetime

from pydantic import BaseModel, Field

from vehicle_counter.app.server.models.direction import DirectionSchema


class HistoryRegistrySchema(BaseModel):
    total_cars: int = Field(..., gt=0)
    total_buses: int = Field(..., gt=0)
    total_trucks: int = Field(..., gt=0)
    total_motorbikes: int = Field(..., gt=0)
    co2_impact: float = Field(...)

    up: DirectionSchema = None
    down: DirectionSchema = None

    timestamp: datetime = Field(...)
