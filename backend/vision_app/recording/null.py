from vision_app.domain import DomainEvent, Frame, InferenceResult
from vision_app.recording.base import Recorder


class NullRecorder(Recorder):
    def record(
        self,
        frame: Frame,
        result: InferenceResult,
        events: list[DomainEvent],
    ) -> None:
        return None
