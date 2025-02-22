# app/routers/dataset.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from app.utils.file_handler import save_file
from app.models.database_models import DatasetModel
from app.models.schema import DatasetListResponse, DatasetInfo
from app.utils.database import get_db
from bson import ObjectId

router = APIRouter()


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
