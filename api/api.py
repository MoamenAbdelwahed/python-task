from fastapi import APIRouter, File, UploadFile, Query
from infrastructure.mongodb import MONGO_REPO
from core.services import process_images, get_images

router = APIRouter()

@router.post("/process-images")
async def process_images(csv_file: UploadFile = File(...)):
    """Endpoint to receive CSV data and trigger image processing."""

    try:
        result = await process_images(csv_file)
        return result
    except Exception as e:
        return {"error": str(e)}, 500

@router.get("/images")
async def get_all_grayscale_images(depth_min: float = Query(None), depth_max: float = Query(None)):
    images_data = await get_images(depth_min, depth_max)

    return images_data