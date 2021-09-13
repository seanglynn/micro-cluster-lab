from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    retrieve_users_ts,
    update_user,
    retrieve_browser_stats,
    retrieve_os_stats,
)
from app.server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
)

router = APIRouter()


@router.get("/browser", response_description="Browser Data Retrieved")
async def get_browser_stats():
    browser_stats = await retrieve_browser_stats()
    if browser_stats:
        return ResponseModel(browser_stats, "Browser data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.get("/os", response_description="OS Data Retrieved")
async def get_os_stats():
    os_stats = await retrieve_os_stats()
    if os_stats:
        return ResponseModel(os_stats, "OS data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")



