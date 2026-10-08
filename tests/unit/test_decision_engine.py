import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))

from vision_app.decision.engine import DecisionConfig, DecisionEngine
from vision_app.decision.state import InspectionState
from vision_app.domain import Detection, InferenceResult


def result(frame_id: int, class_name: str = "target") -> InferenceResult:
    return InferenceResult(
        camera_id="test",
        frame_id=frame_id,
        timestamp_ns=frame_id,
        detections=(Detection(class_name=class_name, confidence=0.99),),
    )


def ready(engine: DecisionEngine) -> None:
    for frame_id in range(1, 4):
        engine.update(result(frame_id), {"trigger": True})
    assert engine.state == InspectionState.READY


def test_pass_after_full_window():
    engine = DecisionEngine(DecisionConfig())
    ready(engine)

    events = []
    for frame_id in range(4, 9):
        events += engine.update(result(frame_id, "target"), {"trigger": True})

    assert engine.state == InspectionState.PASS
    assert any(
        e.name == "inspection.completed" and e.payload["result"] == "PASS"
        for e in events
    )


def test_fail_after_reject_threshold():
    engine = DecisionEngine(DecisionConfig())
    ready(engine)

    events = []
    events += engine.update(result(4, "reject"), {"trigger": True})
    events += engine.update(result(5, "reject"), {"trigger": True})

    assert engine.state == InspectionState.FAIL
    assert any(e.name == "alarm.raised" for e in events)


def test_trigger_off_resets_cycle():
    engine = DecisionEngine(DecisionConfig())
    ready(engine)

    events = engine.update(result(4), {"trigger": False})

    assert engine.state == InspectionState.IDLE
    assert any(e.name == "state.changed" for e in events)
