from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str | None = None
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str | None = None
    disabled: bool

    class Config:
        from_attributes = True