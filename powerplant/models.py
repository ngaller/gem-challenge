from enum import Enum
from typing import List, Dict

from pydantic import BaseModel, validator

from powerplant.base_models import PlantBase


class FuelTypeEnum(str, Enum):
    gas = 'gas'
    kerosine = 'kerosine'
    wind = 'wind'


class Fuel(BaseModel):
    # € / MWh
    cost: float
    # % of wind, or 1 for gas
    factor: float


class Plant(PlantBase):
    # refers to Fuel.type
    fuel_type: str


class Problem(BaseModel):
    load: float
    fuels: Dict[FuelTypeEnum, Fuel]
    powerplants: List[Plant]

    @validator('powerplants')
    def must_have_defined_fuel(cls, v, values):
        assert all(plant.fuel_type in values['fuels'] for plant in v)
        return v


class PlantConfiguration(BaseModel):
    name: str
    p: float
