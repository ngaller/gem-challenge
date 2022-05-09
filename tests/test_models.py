import pytest
from pydantic import ValidationError

from powerplant.models import Plant, Problem, FuelTypeEnum


def test_problem_validates_defined_fuel():
    with pytest.raises(ValidationError):
        Problem(
            load=50,
            fuels={
            },
            powerplants=[
                Plant(
                    name="1",
                    fuel_type=FuelTypeEnum.gas,
                    efficiency=1,
                    pmin=10,
                    pmax=10
                )
            ]
        )
