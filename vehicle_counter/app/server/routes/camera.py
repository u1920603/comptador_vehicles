from fastapi import APIRouter

from vehicle_counter.app.server.database import retrieve_cameras
from vehicle_counter.app.server.models.camera import ResponseModel

router = APIRouter()


@router.get("/", response_description="Camera retrieved")
async def get_students():
    cameras = await retrieve_cameras()
    if cameras:
        return ResponseModel(cameras, "Cameras data retrieved successfully")
    return ResponseModel(cameras, "Empty list returned")
