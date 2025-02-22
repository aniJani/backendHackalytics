from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


# Helper class to work with MongoDB ObjectIds
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class DatasetModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    file_path: str
    filename: str
    user_id: str = "user1"  # Defaults to user1

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class VisualizationModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    code: str
    dataset_id: str
    description: Optional[str] = None
    user_id: str = "user1"  # Defaults to user1

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
