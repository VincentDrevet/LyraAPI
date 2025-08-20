from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
from typing import Optional

class NewAclModel(BaseModel):
    topic: str
    permission: Literal[0, 1, 2, 4]

class ReturnNewAclModel(BaseModel):
    id: int
    topic: str
    permission: int
    device_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

class GetAclModel(BaseModel):
    id: int
    topic: str
    permission: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    device_id: int

class AclCheck(BaseModel):
    username: str
    clientid: str
    topic: str
    acc: int
