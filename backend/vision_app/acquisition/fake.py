from time import time_ns

import numpy as np

from vision_app.acquisition.base import FrameSource
from vision_app.domain import Frame


class FakeCamera(FrameSource):
    def __init__(self, camera_id: str = "demo", width: int = 640, height: int = 480):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.frame_id = 0
        self.is_open = False

    def open(self) -> None:
        self.is_open = True

    def read(self) -> Frame:
        if not self.is_open:
            self.open()
        self.frame_id += 1
        value = self.frame_id % 255
        image = np.full((self.height, self.width, 3), value, dtype=np.uint8)
        return Frame(
            camera_id=self.camera_id,
            frame_id=self.frame_id,
            timestamp_ns=time_ns(),
            image=image,
        )

    def close(self) -> None:
        self.is_open = False
