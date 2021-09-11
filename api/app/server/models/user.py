from typing import Optional

from pydantic import BaseModel, EmailStr, Field

# root
#  |-- date: string (nullable = true)
#  |-- time: string (nullable = true)
#  |-- user_id: string (nullable = true)
#  |-- url: string (nullable = true)
#  |-- ip: string (nullable = true)
#  |-- user_agent_str: string (nullable = true)
#  |-- ip_shortened: string (nullable = false)
#  |-- network: string (nullable = true)
#  |-- city_name: string (nullable = true)
#  |-- country_name: string (nullable = true)

class UserSchema(BaseModel):
    user_id: str = Field(...) #TODO - Check unique docid
    url: str = Field(...)
    ip: str = Field(...)
    browser_family: str = Field(...)
    os: str = Field(...)
    city: str = Field(...)
    country: str = Field(...)
    # email: EmailStr = Field(...)
    # course_of_study: str = Field(...)
    # year: int = Field(..., gt=0, lt=9)
    # gpa: float = Field(..., le=4.0)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "7bba30036f806bf61bffafdb7f22157c218ed791",
                "url": "http://35f1b09dbc2ed8eb547d1e1fb62037cf212d59a8/7384adb1cfd82021c125a55d019aa235b12c5208",
                "ip": "154.50.192.153",
                "browser_family": "Mozilla/5.0",
                "os": "Windows NT 6.1",
                "city": "New York",
                "country": "United States",
            }
        }


class UpdateUserModel(BaseModel):
    user_id: str = Field(...) #TODO - Check unique docid
    url: str = Field(...)
    ip: str = Field(...)
    browser_family: str = Field(...)
    os: str = Field(...)
    city: str = Field(...)
    country: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "7bba30036f806bf61bffafdb7f22157c218ed791",
                "url": "http://35f1b09dbc2ed8eb547d1e1fb62037cf212d59a8/7384adb1cfd82021c125a55d019aa235b12c5208",
                "ip": "154.50.192.153",
                "browser_family": "Mozilla/5.0",
                "os": "Windows NT 6.1",
                "city": "New York",
                "country": "United States",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
