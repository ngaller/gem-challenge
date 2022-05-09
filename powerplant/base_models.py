from pydantic.dataclasses import dataclass


@dataclass
class PlantBase:
    name: str
    # 1 for wind
    efficiency: float
    pmin: float
    pmax: float
