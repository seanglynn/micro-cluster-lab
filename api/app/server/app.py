from fastapi import FastAPI

from app.server.routes.user import router as UserRouter
from app.server.routes.stats import router as StatsRouter

app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(StatsRouter, tags=["Stats"], prefix="/stats")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": {"Check out:": {
        "user mapping": "/user",
        "stats mapping": "/stats",
    }}
    }
