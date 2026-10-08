from abc import ABC, abstractmethod

from vision_app.domain import Frame, InferenceResult


class InferenceEngine(ABC):
    @abstractmethod
    def infer(self, frame: Frame) -> InferenceResult:
        """Convert an image frame into a canonical inference result."""
