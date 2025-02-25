from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from app.utils.file_handler import save_file
from app.models.database_models import DatasetModel
from app.models.schema import DatasetListResponse, DatasetInfo
from app.services.visualization_service import analyze_dataset
from app.utils.database import get_db
from bson import ObjectId
import math

router = APIRouter()


def clean_data(data):
    """
    Recursively cleans data by replacing non-finite floats (NaN, Infinity) with None.
    """
    if isinstance(data, float):
        # If the float is finite, return it; otherwise return None.
        return data if math.isfinite(data) else None
    elif isinstance(data, dict):
        return {k: clean_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_data(item) for item in data]
    else:
        return data


@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    user_id: str = Form("user1"),  # Defaults to user1 if not provided
):
    file_location = await save_file(file)
    # Create a new dataset record
    dataset = DatasetModel(
        file_path=file_location, filename=file.filename, user_id=user_id
    )

    db = get_db()
    # Remove _id from the dict so that MongoDB will generate one
    dataset_data = dataset.dict(by_alias=True)
    dataset_data.pop("_id", None)

    result = await db.datasets.insert_one(dataset_data)
    return {"message": "Dataset uploaded successfully", "id": str(result.inserted_id)}


@router.get("/list", response_model=DatasetListResponse)
async def list_datasets(
    user_id: str = Query("user1", description="User id, defaults to user1")
):
    db = get_db()
    cursor = db.datasets.find({"user_id": user_id})
    datasets = []
    async for dataset in cursor:
        # Convert the MongoDB ObjectId to string for the response
        datasets.append(
            DatasetInfo(
                id=str(dataset["_id"]),
                file_path=dataset["file_path"],
                filename=dataset["filename"],
                user_id=dataset["user_id"],
            )
        )
    return DatasetListResponse(datasets=datasets)


@router.get("/head")
async def get_dataset_head(
    dataset_id: str = Query(..., description="ID of the dataset")
):
    db = get_db()
    # Find the dataset record by its ObjectId
    dataset = await db.datasets.find_one({"_id": ObjectId(dataset_id)})
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    file_path = dataset["file_path"]
    try:
        # analyze_dataset returns a summary and the DataFrame.
        summary, _ = analyze_dataset(file_path)
        # Clean the summary data to ensure all float values are JSON compliant.
        summary = clean_data(summary)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error analyzing dataset: {str(e)}"
        )

    return summary
