from fastapi import FastAPI

from app.server.routes.student import router as StudentRouter
# from app.server.routes.user import router as UserRouter

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")
## TODO - Implement Users route
# app.include_router(UserRouter, tags=["User"], prefix="/user")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
