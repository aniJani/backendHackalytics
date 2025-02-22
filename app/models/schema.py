# app/models/schema.py
from pydantic import BaseModel
from typing import Optional, List


class DatasetInfo(BaseModel):
    id: str
    file_path: str
    filename: str
    user_id: str


class DatasetListResponse(BaseModel):
    datasets: List[DatasetInfo]


class ChatRequest(BaseModel):
    message: str
    user_id: str = "user1"


class VisualizationRequest(BaseModel):
    dataset_id: str
    prompt: Optional[str] = "Generate a visualization for the given dataset."
    user_id: str = "user1"


class VisualizationResponse(BaseModel):
    code: str
    image_base64: str
    description: Optional[str] = None


class InsightRequest(BaseModel):
    query: str
    dataset_id: str  # Now required to specify which dataset to use
    user_id: str = "user1"


class InsightResponse(BaseModel):
    insights: str


class ReRunVisualizationResponse(BaseModel):
    visualizations: List[VisualizationResponse]
