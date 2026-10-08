from abc import ABC, abstractmethod


class MachineIO(ABC):
    @abstractmethod
    def read_inputs(self) -> dict[str, bool]:
        ...

    @abstractmethod
    def write_output(self, name: str, value: bool) -> None:
        ...
