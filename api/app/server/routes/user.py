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


@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@router.get("/", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    # print(users)
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/{id}", response_description="User data retrieved")
async def get_user_data(id):
    print(id)
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.get("/search?start_date={ts_start}&end_date={ts_end}", response_description="User data retrieved")
async def get_user_data_ts(ts_start, ts_end):
    users_ts = await retrieve_users_ts(ts_start, 5)
    if users_ts:
        return ResponseModel(users_ts, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.get("/stats/browser", response_description="Browser Data Retrieved")
async def get_browser_stats():
    browser_stats = await retrieve_browser_stats()
    if browser_stats:
        return ResponseModel(browser_stats, "Browser data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.get("/stats/os", response_description="OS Data Retrieved")
async def get_os_stats():
    os_stats = await retrieve_os_stats()
    if os_stats:
        return ResponseModel(os_stats, "OS data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")



@router.put("/{id}")
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id, req)
    if updated_user:
        return ResponseModel(
            "User with ID: {} name update is successful".format(id),
            "User name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )
