from dataclasses import dataclass


@dataclass(frozen=True)
class DataContainer:
    data: str
    source: str
