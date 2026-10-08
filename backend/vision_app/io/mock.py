from vision_app.io.base import MachineIO


class MockIO(MachineIO):
    def __init__(self):
        self.inputs: dict[str, bool] = {"trigger": False}
        self.outputs: dict[str, bool] = {}

    def read_inputs(self) -> dict[str, bool]:
        return dict(self.inputs)

    def write_output(self, name: str, value: bool) -> None:
        self.outputs[name] = value

    def set_input(self, name: str, value: bool) -> None:
        self.inputs[name] = value
