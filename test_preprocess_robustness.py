import sys
import asyncio
import numpy as np
sys.path.insert(0, r'services\preprocessing')

# Mock image_io to return a dummy image instead of reading from disk
from types import ModuleType
vision_utils = ModuleType('libs.vision_utils')
image_io = ModuleType('libs.vision_utils.image_io')
image_io.load_image_from_path = lambda p: np.zeros((720, 1280, 3), dtype=np.uint8)
image_io.encode_image_to_jpg_bytes = lambda img: b"fake_jpg_bytes"
sys.modules['libs.vision_utils'] = vision_utils
sys.modules['libs.vision_utils.image_io'] = image_io

from app.services.preprocess_service import preprocess_frame
from app.api.schemas import PreprocessRequest

async def run():
    req = PreprocessRequest(
        frame_id="frame-123",
        camera_id="cam-01",
        timestamp="2026-06-20T10:00:00Z",
        storage_path="raw_frames/cam-01/frame-123.jpg"
    )
    res = await preprocess_frame(req)
    print("Metrics:", res["metrics"])
    print("Conditions Detected:", res["conditions_detected"])
    print("Plan Applied:", res["plan_applied"])

asyncio.run(run())
