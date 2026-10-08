from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np


@dataclass(slots=True)
class Frame:
    camera_id: str
    frame_id: int
    timestamp_ns: int
    image: np.ndarray


@dataclass(slots=True, frozen=True)
class Detection:
    class_name: str
    confidence: float
    bbox: tuple[float, float, float, float] | None = None
    polygon: tuple[tuple[float, float], ...] | None = None


@dataclass(slots=True, frozen=True)
class InferenceResult:
    camera_id: str
    frame_id: int
    timestamp_ns: int
    detections: tuple[Detection, ...]
    latency_ms: float = 0.0


@dataclass(slots=True, frozen=True)
class DomainEvent:
    name: str
    payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "payload": self.payload}


def inference_to_dict(result: InferenceResult) -> dict[str, Any]:
    return {
        "camera_id": result.camera_id,
        "frame_id": result.frame_id,
        "timestamp_ns": result.timestamp_ns,
        "latency_ms": result.latency_ms,
        "detections": [asdict(d) for d in result.detections],
    }
