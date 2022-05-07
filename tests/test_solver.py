from src.models import Problem, Plant, Fuel, PlantConfiguration
from src.solver import solve, merit_order


def test_sort_merit_order():
    plants = [
        Plant(name="1", fuel_type="gas", efficiency=.43),
        Plant(name="4", fuel_type="gas", efficiency=.5),
        Plant(name="3", fuel_type="kerosine", efficiency=.3),
        Plant(name="2", fuel_type="wind", efficiency=1),
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
        plants=[
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
        plants=[
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
        plants=[
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
        plants=[
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
        plants=[
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
        plants=[
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
