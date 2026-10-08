from time import perf_counter

from vision_app.domain import Detection, Frame, InferenceResult
from vision_app.inference.base import InferenceEngine


class FakeInferenceEngine(InferenceEngine):
    def __init__(self, reject_every_n_frames: int = 0):
        self.reject_every_n_frames = reject_every_n_frames

    def infer(self, frame: Frame) -> InferenceResult:
        begin = perf_counter()
        is_reject = (
            self.reject_every_n_frames > 0
            and frame.frame_id % self.reject_every_n_frames == 0
        )
        class_name = "reject" if is_reject else "target"
        detection = Detection(class_name=class_name, confidence=0.99)
        return InferenceResult(
            camera_id=frame.camera_id,
            frame_id=frame.frame_id,
            timestamp_ns=frame.timestamp_ns,
            detections=(detection,),
            latency_ms=(perf_counter() - begin) * 1000,
        )
