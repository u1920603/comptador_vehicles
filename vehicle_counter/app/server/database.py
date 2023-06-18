import motor.motor_asyncio

MONGO_DETAILS = "mongodb://mongodb:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.vehicle_counter

camera_collection = database.get_collection("camera")


# helpers
def camera_helper(camera) -> dict:
    return {
        "id": str(camera["_id"]),
        "created_at": camera["created_at"],
        "updated_at": camera["updated_at"],
        "location": camera["location"],
        "measurements": camera["measurements"],
    }


async def retrieve_cameras():
    cameras = []
    async for student in camera_collection.find():
        cameras.append(camera_helper(student))
    return cameras
