from __future__ import annotations

from dataclasses import dataclass

from vision_app.decision.state import InspectionState
from vision_app.domain import DomainEvent, InferenceResult


@dataclass(slots=True, frozen=True)
class DecisionConfig:
    target_class: str = "target"
    reject_class: str = "reject"
    ready_consecutive_frames: int = 3
    window_frames: int = 5
    reject_threshold: int = 2


class DecisionEngine:
    """Pure inspection-cycle logic with no Redis, camera, or PLC dependency."""

    def __init__(self, config: DecisionConfig):
        self.config = config
        self.state = InspectionState.IDLE
        self._trigger_count = 0
        self._judged_frames = 0
        self._reject_count = 0

    def reset(self) -> list[DomainEvent]:
        old = self.state
        self.state = InspectionState.IDLE
        self._trigger_count = 0
        self._judged_frames = 0
        self._reject_count = 0
        if old == InspectionState.IDLE:
            return []
        return [DomainEvent("state.changed", {"from": old, "to": self.state})]

    def update(
        self,
        result: InferenceResult,
        sensor_state: dict[str, bool],
    ) -> list[DomainEvent]:
        events: list[DomainEvent] = []
        trigger = bool(sensor_state.get("trigger", False))

        if not trigger:
            return self.reset()

        if self.state == InspectionState.IDLE:
            self._trigger_count += 1
            if self._trigger_count >= self.config.ready_consecutive_frames:
                old = self.state
                self.state = InspectionState.READY
                events.append(DomainEvent("state.changed", {"from": old, "to": self.state}))
            return events

        classes = {d.class_name for d in result.detections}
        has_inspection_target = bool(
            classes & {self.config.target_class, self.config.reject_class}
        )

        if self.state == InspectionState.READY and has_inspection_target:
            old = self.state
            self.state = InspectionState.JUDGING
            events.extend(
                [
                    DomainEvent("state.changed", {"from": old, "to": self.state}),
                    DomainEvent("inspection.started", {"frame_id": result.frame_id}),
                ]
            )

        if self.state != InspectionState.JUDGING or not has_inspection_target:
            return events

        self._judged_frames += 1
        if self.config.reject_class in classes:
            self._reject_count += 1

        if self._reject_count >= self.config.reject_threshold:
            self.state = InspectionState.FAIL
            events.extend(
                [
                    DomainEvent(
                        "alarm.raised",
                        {
                            "code": "inspection_reject",
                            "frame_id": result.frame_id,
                            "reject_count": self._reject_count,
                        },
                    ),
                    DomainEvent(
                        "inspection.completed",
                        {"result": "FAIL", "frame_id": result.frame_id},
                    ),
                ]
            )
        elif self._judged_frames >= self.config.window_frames:
            self.state = InspectionState.PASS
            events.append(
                DomainEvent(
                    "inspection.completed",
                    {"result": "PASS", "frame_id": result.frame_id},
                )
            )

        return events

    def snapshot(self) -> dict[str, int | str]:
        return {
            "state": self.state,
            "trigger_count": self._trigger_count,
            "judged_frames": self._judged_frames,
            "reject_count": self._reject_count,
        }
