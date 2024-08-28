from pydantic import BaseModel, Field, ConfigDict


class UserAdd(BaseModel):
    username: str = Field(min_length=4, max_length=15)
    password: str


class UserOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
