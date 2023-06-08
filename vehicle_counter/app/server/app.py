from fastapi import FastAPI

from vehicle_counter.app.server.routes.camera import router as CameraRouter

app = FastAPI()

app.include_router(CameraRouter, tags=["Camera"], prefix="/camera")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the vehicle counter API"}
