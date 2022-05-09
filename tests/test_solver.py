import pytest
from powerplant.models import Problem, Plant, Fuel, PlantConfiguration
from powerplant.solver import solve, merit_order


def test_sort_merit_order():
    plants = [
        Plant(name="1", fuel_type="gas", efficiency=.43, pmax=0, pmin=0),
        Plant(name="4", fuel_type="gas", efficiency=.5, pmax=0, pmin=0),
        Plant(name="3", fuel_type="kerosine", efficiency=.3, pmax=0, pmin=0),
        Plant(name="2", fuel_type="wind", efficiency=1, pmax=0, pmin=0),
    ]
    fuels = {
        "wind": Fuel(cost=0, factor=.5),
        "gas": Fuel(cost=1, factor=1),
        "kerosine": Fuel(cost=2, factor=1),
    }
    sorted_plants = sorted(plants, key=merit_order(fuels))
    assert [p.name for p in sorted_plants] == ["2", "4", "1", "3"]


def test_solve_trivial():
    problem = Problem(
        fuels={
            "gas": Fuel(cost=1, factor=1)
        },
        powerplants=[
            Plant(name="gas1", fuel_type="gas", efficiency=.5, pmin=10, pmax=100)
        ],
        load=100
    )
    solution = solve(problem)
    assert solution == [
        PlantConfiguration(name="gas1", p=100)
    ]


def test_solve_2_gas_plants():
    problem = Problem(
        fuels={
            "gas": Fuel(cost=1, factor=1)
        },
        powerplants=[
            Plant(name="gas1", fuel_type="gas", efficiency=.48, pmin=10, pmax=100),
            Plant(name="gas2", fuel_type="gas", efficiency=.53, pmin=10, pmax=100)
        ],
        load=100
    )
    solution = solve(problem)
    assert solution == [
        PlantConfiguration(name="gas2", p=100),
        PlantConfiguration(name="gas1", p=0.0),
    ]


def test_solve_2_fuels():
    problem = Problem(
        fuels={
            "gas": Fuel(cost=1, factor=1),
            "kerosine": Fuel(cost=2, factor=1),
            "wind": Fuel(cost=0, factor=.5),
        },
        powerplants=[
            Plant(name="kerosine", fuel_type="gas", efficiency=.3, pmin=10, pmax=100),
            Plant(name="gas1", fuel_type="gas", efficiency=.43, pmin=10, pmax=100),
            Plant(name="gas2", fuel_type="gas", efficiency=.58, pmin=10, pmax=100),
        ],
        load=100
    )
    solution = solve(problem)
    assert solution == [
        PlantConfiguration(name="gas2", p=100),
        PlantConfiguration(name="gas1", p=0.0),
        PlantConfiguration(name="kerosine", p=0.0),
    ]


def test_solve_2_plants():
    problem = Problem(
        fuels={
            "gas": Fuel(cost=1, factor=1),
            "kerosine": Fuel(cost=2, factor=1),
            "wind": Fuel(cost=0, factor=.5),
        },
        powerplants=[
            Plant(name="kerosine", fuel_type="gas", efficiency=.3, pmin=10, pmax=100),
            Plant(name="gas1", fuel_type="gas", efficiency=.43, pmin=10, pmax=100),
            Plant(name="gas2", fuel_type="gas", efficiency=.58, pmin=10, pmax=100),
        ],
        load=200
    )
    solution = solve(problem)
    assert solution == [
        PlantConfiguration(name="gas2", p=100),
        PlantConfiguration(name="gas1", p=100),
        PlantConfiguration(name="kerosine", p=0.0),
    ]


def test_solve_2_plants_not_max_power():
    problem = Problem(
        fuels={
            "gas": Fuel(cost=1, factor=1),
            "kerosine": Fuel(cost=2, factor=1),
            "wind": Fuel(cost=0, factor=.5),
        },
        powerplants=[
            Plant(name="kerosine", fuel_type="gas", efficiency=.3, pmin=10, pmax=100),
            Plant(name="gas1", fuel_type="gas", efficiency=.43, pmin=10, pmax=100),
            Plant(name="gas2", fuel_type="gas", efficiency=.58, pmin=10, pmax=100),
        ],
        load=150
    )
    solution = solve(problem)
    assert solution == [
        PlantConfiguration(name="gas2", p=100),
        PlantConfiguration(name="gas1", p=50),
        PlantConfiguration(name="kerosine", p=0.0),
    ]


def test_solve_wind_simple():
    problem = Problem(
        fuels={
            "gas": Fuel(cost=1, factor=1),
            "kerosine": Fuel(cost=2, factor=1),
            "wind": Fuel(cost=0, factor=1),
        },
        powerplants=[
            Plant(name="kerosine", fuel_type="gas", efficiency=.3, pmin=10, pmax=100),
            Plant(name="gas1", fuel_type="gas", efficiency=.43, pmin=10, pmax=100),
            Plant(name="gas2", fuel_type="gas", efficiency=.58, pmin=10, pmax=100),
            Plant(name="wind1", fuel_type="wind", efficiency=1, pmin=10, pmax=10),
        ],
        load=150
    )
    solution = solve(problem)
    assert solution == [
        PlantConfiguration(name="wind1", p=10),
        PlantConfiguration(name="gas2", p=100),
        PlantConfiguration(name="gas1", p=40),
        PlantConfiguration(name="kerosine", p=0.0),
    ]


def test_solve_wind_not_full_wind():
    problem = Problem(
        fuels={
            "gas": Fuel(cost=1, factor=1),
            "kerosine": Fuel(cost=2, factor=1),
            "wind": Fuel(cost=0, factor=.8),
        },
        powerplants=[
            Plant(name="kerosine", fuel_type="gas", efficiency=.3, pmin=10, pmax=100),
            Plant(name="gas1", fuel_type="gas", efficiency=.43, pmin=5, pmax=100),
            Plant(name="gas2", fuel_type="gas", efficiency=.58, pmin=10, pmax=100),
            Plant(name="wind1", fuel_type="wind", efficiency=1, pmin=10, pmax=10),
            Plant(name="wind2", fuel_type="wind", efficiency=1, pmin=10, pmax=10),
        ],
        load=15
    )
    solution = solve(problem)
    assert solution == [
        PlantConfiguration(name="wind1", p=8.0),
        PlantConfiguration(name="wind2", p=0.0),
        PlantConfiguration(name="gas2", p=0.0),
        PlantConfiguration(name="gas1", p=7),
        PlantConfiguration(name="kerosine", p=0.0),
    ]


def test_solve_wind_not_all_plants():
    problem = Problem(
        fuels={
            "gas": Fuel(cost=1, factor=1),
            "kerosine": Fuel(cost=2, factor=1),
            "wind": Fuel(cost=0, factor=1),
        },
        powerplants=[
            Plant(name="kerosine", fuel_type="gas", efficiency=.3, pmin=10, pmax=100),
            Plant(name="gas1", fuel_type="gas", efficiency=.43, pmin=10, pmax=100),
            Plant(name="gas2", fuel_type="gas", efficiency=.58, pmin=10, pmax=100),
            Plant(name="wind1", fuel_type="wind", efficiency=1, pmin=10, pmax=10),
            Plant(name="wind2", fuel_type="wind", efficiency=1, pmin=10, pmax=10),
        ],
        load=15
    )
    solution = solve(problem)
    assert solution == [
        PlantConfiguration(name="wind1", p=0.0),
        PlantConfiguration(name="wind2", p=0.0),
        PlantConfiguration(name="gas2", p=15),
        PlantConfiguration(name="gas1", p=0.0),
        PlantConfiguration(name="kerosine", p=0.0),
    ]


def test_solve_pathological_backtracking():
    # in this test the instance that is least likely to be chosen (the kerosine fueled plant)
    # ends up being the only suitable one, so a naive approach will fail to compute in time
    # as it will have to explore every single solution
    problem = Problem(
        fuels={
            "gas": Fuel(cost=1, factor=1),
            "kerosine": Fuel(cost=2, factor=1),
            "wind": Fuel(cost=0, factor=1),
        },
        powerplants=[
                   Plant(name="kerosine", fuel_type="gas", efficiency=.3, pmin=10, pmax=100),
                   Plant(name="wind1", fuel_type="wind", efficiency=1, pmin=10, pmax=10),
               ] + [
                   Plant(name="gas2", fuel_type="gas", efficiency=.58, pmin=20, pmax=100),
               ] * 50,
        load=15
    )
    solution = solve(problem)
    assert solution[-1] == PlantConfiguration(name="kerosine", p=15)


def test_solve_not_possible():
    problem = Problem(
        fuels={
            "gas": Fuel(cost=1, factor=1),
            "wind": Fuel(cost=0, factor=1),
        },
        powerplants=[
            Plant(name="wind", fuel_type="wind", efficiency=1, pmin=20, pmax=20),
            Plant(name="gas1", fuel_type="gas", efficiency=.43, pmin=50, pmax=100),
        ],
        load=15
    )
    with pytest.raises(ValueError):
        solve(problem)
