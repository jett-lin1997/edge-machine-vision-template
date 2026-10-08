from abc import ABC, abstractmethod

from vision_app.domain import Frame


class FrameSource(ABC):
    @abstractmethod
    def open(self) -> None:
        """Acquire resources."""

    @abstractmethod
    def read(self) -> Frame:
        """Return the next frame."""

    @abstractmethod
    def close(self) -> None:
        """Release resources."""
