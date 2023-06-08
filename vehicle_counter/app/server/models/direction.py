from pydantic import BaseModel, Field


class DirectionSchema(BaseModel):
    total_cars: int = Field(..., gt=0)
    total_buses: int = Field(..., gt=0)
    total_trucks: int = Field(..., gt=0)
    total_motorbikes: int = Field(..., gt=0)

    class Config:
        schema_extra = {
            "example": {
                "total_cars": 1,
                "total_buses": 3,
                "total_trucks": 4,
                "total_motorbikes": 2
            }
        }
