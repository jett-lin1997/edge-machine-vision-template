import json

from redis import Redis


class RedisStateRepository:
    def __init__(self, client: Redis, namespace: str = "vision"):
        self.client = client
        self.namespace = namespace

    def _key(self, name: str) -> str:
        return f"{self.namespace}:{name}"

    def ping(self) -> bool:
        return bool(self.client.ping())

    def set_json(self, name: str, value: dict) -> None:
        self.client.set(self._key(name), json.dumps(value, default=str))

    def get_json(self, name: str) -> dict | None:
        raw = self.client.get(self._key(name))
        if raw is None:
            return None
        if isinstance(raw, bytes):
            raw = raw.decode()
        return json.loads(raw)

    def publish(self, channel: str, event: dict) -> None:
        self.client.publish(self._key(channel), json.dumps(event, default=str))
