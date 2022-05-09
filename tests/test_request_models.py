from powerplant.models import FuelTypeEnum
from powerplant.request_models import ProblemRequest, PlantRequest, PlantTypeEnum


def test_to_problem():
    problem = ProblemRequest(
        load=50,
        fuels={
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60
        },
        powerplants=[
            PlantRequest(
                name="1",
                type=PlantTypeEnum.gasfired,
                efficiency=1,
                pmin=10,
                pmax=10
            )
        ]
    )
    result = problem.to_problem()
    assert result.fuels.keys() == {"gas", "wind", "kerosine"}
    assert result.fuels[FuelTypeEnum.wind].factor == .6
    assert result.load == 50
    assert len(result.powerplants) == 1
    assert result.powerplants[0].fuel_type == FuelTypeEnum.gas
