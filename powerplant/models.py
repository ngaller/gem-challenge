from pydantic.dataclasses import dataclass
from typing import List, Dict

from powerplant.base_models import PlantBase


@dataclass
class Fuel:
    # € / MWh
    cost: float
    # % of wind, or 1 for gas
    factor: float


@dataclass
class Plant(PlantBase):
    # refers to Fuel.type
    fuel_type: str


@dataclass
class Problem:
    load: float
    fuels: Dict[str, Fuel]
    powerplants: List[Plant]


@dataclass
class PlantConfiguration:
    name: str
    p: float
