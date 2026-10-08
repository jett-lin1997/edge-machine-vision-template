from vision_app.acquisition.base import FrameSource
from vision_app.decision.engine import DecisionEngine
from vision_app.domain import inference_to_dict
from vision_app.inference.base import InferenceEngine
from vision_app.io.base import MachineIO
from vision_app.repositories.redis_state import RedisStateRepository


class VisionPipeline:
    def __init__(
        self,
        source: FrameSource,
        inference: InferenceEngine,
        decision: DecisionEngine,
        machine_io: MachineIO,
        state_repo: RedisStateRepository,
    ):
        self.source = source
        self.inference = inference
        self.decision = decision
        self.machine_io = machine_io
        self.state_repo = state_repo

    def step(self) -> dict:
        frame = self.source.read()
        result = self.inference.infer(frame)
        events = self.decision.update(result, self.machine_io.read_inputs())

        for event in events:
            if event.name == "alarm.raised":
                self.machine_io.write_output("alarm", True)
            self.state_repo.publish("event", event.to_dict())

        payload = {
            "frame_id": frame.frame_id,
            "inference": inference_to_dict(result),
            "decision": self.decision.snapshot(),
            "events": [event.to_dict() for event in events],
        }
        self.state_repo.set_json("inspection:current", payload)
        return payload
