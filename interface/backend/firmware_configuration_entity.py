from dataclasses import dataclass

@dataclass
class FirmwareConfiguration:
    speed: int

    def __init__(self) -> None:
        super().__init__()
        self.speed = 0