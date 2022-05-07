import functools
from typing import List, Dict

from src.models import Problem, PlantConfiguration, Plant, Fuel


def solve(problem: Problem) -> List[PlantConfiguration]:
    plants = sorted(problem.plants, key=merit_order(problem.fuels))
    solution = [0 for _ in plants]
    if _solve_dfs(problem.load, plants, solution):
        powers = _calculate_powers(problem.load, plants, problem.fuels, solution)
        return [
            PlantConfiguration(name=plant.name, p=power)
            for i, (plant, power) in enumerate(zip(plants, powers))
        ]
    raise ValueError("no solution")


def _calculate_powers(load: float, plants: List[Plant], fuels: Dict[str, Fuel], solution):
    # we know the plants are sorted in reverse cost / MW, so we need to turn the lowest ones to the max, if the
    # solution determined that they needed to be switched on
    configuration = [0.0 for _ in plants]
    power = 0
    for i, (p, s) in enumerate(zip(plants, solution)):
        if not s:
            continue
        pmax = p.pmax * fuels[p.fuel_type].factor
        if power + p.pmax < load:
            configuration[i] = pmax
            power += p.pmax
        else:
            configuration[i] = load - power
            return configuration
    raise AssertionError("solution was not valid!")


def _solve_dfs(load, plants, solution, i=0):
    # consider the solution space as a tree, sorted by cost / MW (the nodes on the higher branches have the highest
    # cost) so we want to turn on the plants represented by nodes on the lowest branch first, and only turn them off if
    # this does not yield a solution.
    if i == len(solution):
        return _is_valid_solution(load, plants, solution)
    # start exploring the right branch, since it is cheaper
    solution[i] = 1
    if _solve_dfs(load, plants, solution, i + 1):
        return True
    # ok, didn't work, start exploring the left branch
    solution[i] = 0
    if _solve_dfs(load, plants, solution, i + 1):
        return True
    return False


def _is_valid_solution(load, plants, solution):
    # can we reach the load with the current configuration?
    # TODO take fuel factor into account (for wind)
    pmin = sum(p.pmin * s for (p, s) in zip(plants, solution))
    pmax = sum(p.pmax * s for (p, s) in zip(plants, solution))
    return pmin <= load <= pmax


def merit_order(fuels: Dict[str, Fuel]):
    # build a comparator by merit order
    def comparator(plant1: Plant, plant2: Plant):
        f1 = fuels[plant1.fuel_type]
        f2 = fuels[plant2.fuel_type]
        if f1.cost / plant1.efficiency > f2.cost / plant2.efficiency:
            return 1
        if f1.cost / plant1.efficiency < f2.cost / plant2.efficiency:
            return -1
        return 0

    return functools.cmp_to_key(comparator)
