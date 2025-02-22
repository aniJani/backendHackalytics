from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.models.schema import VisualizationRequest, VisualizationResponse
from app.models.database_models import VisualizationModel
from app.services import openai_service, visualization_service
from app.utils.database import get_db
from fastapi import Query
from app.models.schema import ReRunVisualizationResponse  # see below for this model

router = APIRouter()


@router.post("/generate", response_model=VisualizationResponse)
async def generate_visualization(request: VisualizationRequest):
    db = get_db()
    # Convert dataset_id to ObjectId to query the dataset collection.
    try:
        dataset_obj_id = ObjectId(request.dataset_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid dataset_id format")

    dataset_record = await db.datasets.find_one({"_id": dataset_obj_id})
    if not dataset_record:
        raise HTTPException(status_code=404, detail="Dataset not found")

    file_path = dataset_record["file_path"]

    # Analyze the dataset
    try:
        dataset_summary, _ = visualization_service.analyze_dataset(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error analyzing dataset: {str(e)}"
        )

    # Generate visualization code using the OpenAI API
    try:
        code = openai_service.generate_visualization_code(
            str(dataset_summary), request.prompt
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating code: {str(e)}")

    # Execute the code to produce an image (base64 encoded)
    try:
        image_base64 = visualization_service.execute_visualization_code(code, file_path)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error executing visualization code: {str(e)}"
        )

    # Save the visualization record (remove _id to let MongoDB generate one)
    visualization_record = VisualizationModel(
        code=code,
        dataset_id=request.dataset_id,
        description=request.prompt,
        user_id=request.user_id,
    )
    viz_data = visualization_record.dict(by_alias=True)
    viz_data.pop("_id", None)
    result = await db.visualizations.insert_one(viz_data)
    visualization_record.id = result.inserted_id

    return VisualizationResponse(
        code=code, image_base64=image_base64, description=request.prompt
    )


@router.post("/rerun", response_model=ReRunVisualizationResponse)
async def rerun_visualizations(
    dataset_id: str = Query(
        ..., description="The dataset id (as returned from the upload endpoint)"
    ),
    user_id: str = Query("user1", description="User id, defaults to 'user1'"),
):
    db = get_db()
    # Convert dataset_id string to ObjectId for querying the dataset record.
    try:
        dataset_obj_id = ObjectId(dataset_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid dataset_id format")

    dataset_record = await db.datasets.find_one({"_id": dataset_obj_id})
    if not dataset_record:
        raise HTTPException(status_code=404, detail="Dataset not found")
    file_path = dataset_record["file_path"]

    # Retrieve all visualizations for this dataset and user.
    viz_cursor = db.visualizations.find({"dataset_id": dataset_id, "user_id": user_id})
    visualizations = []
    async for viz in viz_cursor:
        code = viz["code"]
        try:
            # Re-run the code to regenerate the image
            image_base64 = visualization_service.execute_visualization_code(
                code, file_path
            )
        except Exception as e:
            image_base64 = None
        visualizations.append(
            {
                "code": code,
                "image_base64": image_base64,
                "description": viz.get("description", ""),
            }
        )

    return ReRunVisualizationResponse(visualizations=visualizations)
