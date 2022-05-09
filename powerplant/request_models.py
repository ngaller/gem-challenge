# Models used for input to the API
from pydantic.dataclasses import dataclass
from typing import List, Dict

from powerplant.base_models import PlantBase


@dataclass
class Plant(PlantBase):
    type: str


@dataclass
class Problem:
    load: float
    fuels: Dict[str, float]
    powerplants: List[Plant]
