from abc import ABC, abstractmethod

from vision_app.domain import DomainEvent, Frame, InferenceResult


class Recorder(ABC):
    @abstractmethod
    def record(
        self,
        frame: Frame,
        result: InferenceResult,
        events: list[DomainEvent],
    ) -> None:
        """Persist evidence without influencing decision logic."""
