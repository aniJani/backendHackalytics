# app/routers/insights.py
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.models.schema import InsightRequest, InsightResponse
from app.utils.database import get_db
from app.services import insights_service
import os

router = APIRouter()


@router.post("/")
async def get_business_insights(request: InsightRequest):
    db = get_db()
    # Convert dataset_id to ObjectId for querying
    try:
        dataset_obj_id = ObjectId(request.dataset_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid dataset_id format")

    # Retrieve the dataset record for the given user
    dataset_record = await db.datasets.find_one(
        {"_id": dataset_obj_id, "user_id": request.user_id}
    )
    if not dataset_record:
        raise HTTPException(status_code=404, detail="Dataset not found")

    file_path = dataset_record["file_path"]

    # Read the entire dataset as text
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Dataset file not found")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            dataset_text = f.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading dataset: {str(e)}")

    # Generate conversational insights using the entire dataset content
    insights = insights_service.chat_with_assistant(
        messages=[{"role": "user", "content": request.query}],
        dataset_context=dataset_text,
    )

    return InsightResponse(insights=insights)
