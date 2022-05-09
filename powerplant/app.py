from typing import List

from fastapi import FastAPI

from powerplant.models import PlantConfiguration
from powerplant.request_models import Problem

app = FastAPI()


@app.post("/solve", response_model=List[PlantConfiguration])
def solve(problem: Problem):
    return [PlantConfiguration("plant", 0)]
