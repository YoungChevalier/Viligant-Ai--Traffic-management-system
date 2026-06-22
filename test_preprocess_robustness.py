import sys
import asyncio
import numpy as np
from unittest.mock import patch
sys.path.insert(0, r'services\preprocessing')

from app.services.preprocess_service import preprocess_frame
from app.api.schemas import PreprocessRequest

async def run():
    req = PreprocessRequest(
        frame_id="frame-123",
        camera_id="cam-01",
        timestamp="2026-06-20T10:00:00Z",
        storage_path="raw_frames/cam-01/frame-123.jpg"
    )
    with patch('libs.vision_utils.image_io.load_image_from_path', return_value=np.zeros((720, 1280, 3), dtype=np.uint8)), \
         patch('libs.vision_utils.image_io.encode_image_to_jpg_bytes', return_value=b"fake_jpg_bytes"):
        res = await preprocess_frame(req)
        print("Metrics:", res["metrics"])
        print("Conditions Detected:", res["conditions_detected"])
        print("Plan Applied:", res["plan_applied"])

if __name__ == "__main__":
    asyncio.run(run())
