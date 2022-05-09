from typing import List

from fastapi import FastAPI, HTTPException

from powerplant import solver
from powerplant.exceptions import NoSolutionException
from powerplant.models import PlantConfiguration
from powerplant.request_models import ProblemRequest
from powerplant.response_models import ErrorDetail

app = FastAPI()


@app.post("/solve",
          response_model=List[PlantConfiguration],
          responses={
              400: {"description": "Cannot compute a solution for the submission",
                    "model": ErrorDetail}
          })
def solve(problem: ProblemRequest):
    try:
        return solver.solve(problem.to_problem())
    except NoSolutionException as e:
        raise HTTPException(status_code=400, detail=str(e))
