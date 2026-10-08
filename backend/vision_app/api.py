from os import getenv

from fastapi import FastAPI
from pydantic import BaseModel
from redis import Redis

from vision_app.acquisition.fake import FakeCamera
from vision_app.config import load_config
from vision_app.decision.engine import DecisionConfig, DecisionEngine
from vision_app.inference.fake import FakeInferenceEngine
from vision_app.io.mock import MockIO
from vision_app.repositories.redis_state import RedisStateRepository
from vision_app.services.pipeline import VisionPipeline


class DemoStepRequest(BaseModel):
    trigger: bool = True


config = load_config()
redis_client = Redis.from_url(getenv("REDIS_URL", "redis://localhost:6379/0"))
state_repo = RedisStateRepository(redis_client)
machine_io = MockIO()
source = FakeCamera(config.camera_id, config.width, config.height)
inference = FakeInferenceEngine(config.reject_every_n_frames)
decision = DecisionEngine(
    DecisionConfig(
        target_class=config.target_class,
        reject_class=config.reject_class,
        ready_consecutive_frames=config.ready_consecutive_frames,
        window_frames=config.window_frames,
        reject_threshold=config.reject_threshold,
    )
)
pipeline = VisionPipeline(source, inference, decision, machine_io, state_repo)

app = FastAPI(
    title="Edge Machine Vision Template",
    version="0.1.0",
)


@app.get("/api/health")
def health() -> dict:
    try:
        redis_ok = state_repo.ping()
    except Exception as exc:
        return {"status": "degraded", "redis": False, "error": str(exc)}
    return {"status": "ok" if redis_ok else "degraded", "redis": redis_ok}


@app.get("/api/state")
def current_state() -> dict:
    return {
        "project": config.project_name,
        "decision": decision.snapshot(),
        "io": {
            "inputs": machine_io.read_inputs(),
            "outputs": dict(machine_io.outputs),
        },
        "latest": state_repo.get_json("inspection:current"),
    }


@app.post("/api/demo/step")
def demo_step(request: DemoStepRequest) -> dict:
    machine_io.set_input("trigger", request.trigger)
    return pipeline.step()


@app.post("/api/demo/reset")
def demo_reset() -> dict:
    machine_io.set_input("trigger", False)
    decision.reset()
    machine_io.write_output("alarm", False)
    return {"decision": decision.snapshot(), "outputs": dict(machine_io.outputs)}
