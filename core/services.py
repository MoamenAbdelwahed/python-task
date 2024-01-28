from fastapi import UploadFile
import pandas as pd
import numpy as np
from PIL import Image
from infrastructure.mongodb import MONGO_REPO

async def process_images(csv_file: UploadFile):
    """Processes CSV data, resizes images, and stores them in the database."""

    data = pd.read_csv(csv_file.file)

    for depth, image_data in data.groupby("depth"):
        pixels = np.array(image_data.iloc[:, 1:].values, dtype=np.uint8).reshape(-1, 200)
        resized_pixels = np.array(Image.fromarray(pixels).resize((150, pixels.shape[0])))

        document = {
            "depth": depth,
            "image_data": resized_pixels.tolist()
        }
        await MONGO_REPO.create("images", document)

    return {"message": "Images processed and stored successfully"}

async def get_images(depth_min=None, depth_max=None):
    """Retrieves images from the database, optionally filtering by depth."""

    data = await MONGO_REPO.read_all_grayscale("images", depth_min=depth_min, depth_max=depth_max)
    return data
