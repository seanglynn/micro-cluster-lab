from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    timestamp: datetime = Field(...)
    user_id: str = Field(...)
    url: str = Field(...)
    ip: str = Field(...)
    browser: str = Field(...)
    os: str = Field(...)
    os_long: str = Field(...)
    city_name: str = Field(...)
    country_name: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "timestamp": "20141013190433",
                "user_id": "7bba30036f806bf61bffafdb7f22157c218ed791",
                "url": "http://35f1b09dbc2ed8eb547d1e1fb62037cf212d59a8/7384adb1cfd82021c125a55d019aa235b12c5208",
                "ip": "154.50.192.153",
                "browser": "Mozilla/5.0",
                "os": "Windows NT 6.1",
                "city_name": "New York",
                "country_name": "United States",
            }
        }


class UpdateUserModel(BaseModel):
    timestamp: datetime = Field(...)
    user_id: str = Field(...)
    url: str = Field(...)
    ip: str = Field(...)
    browser: str = Field(...)
    os: str = Field(...)
    city_name: str = Field(...)
    country_name: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "timestamp": "20141013190433",
                "user_id": "7bba30036f806bf61bffafdb7f22157c218ed791",
                "url": "http://35f1b09dbc2ed8eb547d1e1fb62037cf212d59a8/7384adb1cfd82021c125a55d019aa235b12c5208",
                "ip": "154.50.192.153",
                "browser": "Mozilla/5.0",
                "os": "Windows NT 6.1",
                "city_name": "New York",
                "country_name": "United States",
            }
        }


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
