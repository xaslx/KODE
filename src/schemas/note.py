from pydantic import BaseModel, Field, ConfigDict


class NoteAdd(BaseModel):
    title: str = Field(min_length=5, max_length=30)
    description: str = Field(min_length=10, max_length=500)


class NoteOut(NoteAdd):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
