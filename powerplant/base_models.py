from pydantic import BaseModel


class PlantBase(BaseModel):
    name: str
    # 1 for wind
    efficiency: float
    pmin: float
    pmax: float
