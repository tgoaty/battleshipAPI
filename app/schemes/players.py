from uuid import UUID

from pydantic import BaseModel

class PlayerRegister(BaseModel):
    username: str
    password: str

class PlayerLogin(BaseModel):
    username: str
    password: str

class PlayerOut(BaseModel):
    sid: UUID
    username: str

    class Config:
        orm_mode = True