# Models used for input to the API
import re
from enum import Enum
from typing import List, Dict

from pydantic import BaseModel, ValidationError

from powerplant.base_models import PlantBase
from powerplant.models import Problem, Fuel, Plant, FuelTypeEnum


class PlantTypeEnum(str, Enum):
    gasfired = 'gasfired'
    turbojet = 'turbojet'
    windturbine = 'windturbine'


_FUEL_BY_PLANT = {
    PlantTypeEnum.gasfired: FuelTypeEnum.gas,
    PlantTypeEnum.turbojet: FuelTypeEnum.kerosine,
    PlantTypeEnum.windturbine: FuelTypeEnum.wind,
}


class PlantRequest(PlantBase):
    type: PlantTypeEnum

    def to_plant(self) -> Plant:
        """Convert to base model"""
        result = Plant(**self.dict(),
                       fuel_type=_FUEL_BY_PLANT[self.type])
        return result


class ProblemRequest(BaseModel):
    load: float
    fuels: Dict[str, float]
    powerplants: List[PlantRequest]

    def to_problem(self) -> Problem:
        """Convert to base model"""
        result = Problem(
            load=self.load,
            fuels={
                re.sub(r'\s*\(.*', '', description): Fuel(
                    cost=value if re.match(r'^gas|kerosine', description) else 0,
                    factor=value / 100.0 if re.match('^wind', description) else 1
                )
                for description, value in self.fuels.items()
                if re.match(r'^wind|gas|kerosine', description)
            },
            powerplants=[
                p.to_plant()
                for p in self.powerplants
            ]
        )
        return result
