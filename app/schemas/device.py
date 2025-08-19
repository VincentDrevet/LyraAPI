from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DeviceAuthValidation(BaseModel):
    client_id: str
    username: str
    password: str

class DeviceCreationModel(BaseModel):
    device_name: str
    username: str

class ReturnNewDeviceModel(BaseModel):
    id: int
    device_name: str
    username: str
    clear_password: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

class GetDeviceModel(BaseModel):
    id: int
    device_name: str
    username: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]