from dataclasses import dataclass
from os import getenv
from pathlib import Path

import yaml


@dataclass(slots=True, frozen=True)
class AppConfig:
    project_name: str
    camera_id: str
    width: int
    height: int
    reject_every_n_frames: int
    target_class: str
    reject_class: str
    ready_consecutive_frames: int
    window_frames: int
    reject_threshold: int


def load_config(path: str | None = None) -> AppConfig:
    config_path = Path(path or getenv("CONFIG_PATH", "/config/default.yaml"))
    data = yaml.safe_load(config_path.read_text())
    return AppConfig(
        project_name=data["project"]["name"],
        camera_id=data["camera"]["id"],
        width=int(data["camera"]["width"]),
        height=int(data["camera"]["height"]),
        reject_every_n_frames=int(data["inference"]["reject_every_n_frames"]),
        target_class=data["decision"]["target_class"],
        reject_class=data["decision"]["reject_class"],
        ready_consecutive_frames=int(data["decision"]["ready_consecutive_frames"]),
        window_frames=int(data["decision"]["window_frames"]),
        reject_threshold=int(data["decision"]["reject_threshold"]),
    )
