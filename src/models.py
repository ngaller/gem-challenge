from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Fuel:
    # € / MWh
    cost: float
    # % of wind, or 1 for gas
    factor: float


@dataclass
class Plant:
    name: str
    # refers to Fuel.type
    fuel_type: str
    # 1 for wind
    efficiency: float = 1
    pmin: float = 0
    pmax: float = 0


@dataclass
class Problem:
    load: float
    fuels: Dict[str, Fuel]
    plants: List[Plant]


@dataclass
class PlantConfiguration:
    name: str
    p: float
