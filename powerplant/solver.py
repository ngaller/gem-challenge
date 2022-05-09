import dataclasses
import functools
from typing import List, Dict, Iterable

from powerplant.models import Problem, PlantConfiguration, Plant, Fuel


def solve(problem: Problem) -> List[PlantConfiguration]:
    plants = _calculate_effective_pminmax(problem.powerplants, problem.fuels)
    plants = sorted(plants, key=merit_order(problem.fuels))
    solution = Solution(plants)
    if _solve_dfs(problem.load, plants, solution):
        powers = solution.calculate_powers(problem.load)
        return [
            PlantConfiguration(name=plant.name, p=power)
            for i, (plant, power) in enumerate(zip(plants, powers))
        ]
    raise ValueError("no solution")


class Solution:
    def __init__(self, plants: List[Plant]):
        self.pmin = 0
        self.pmax = 0
        self.status = [False for _ in plants]
        self.plants = plants

    def add(self, i):
        self.status[i] = True
        self.pmin += self.plants[i].pmin
        self.pmax += self.plants[i].pmax

    def remove(self, i):
        self.status[i] = False
        self.pmin -= self.plants[i].pmin
        self.pmax -= self.plants[i].pmax

    def is_solution(self, load: float):
        return self.pmin <= load <= self.pmax

    def can_solve(self, load: float):
        return self.pmin <= load

    def calculate_powers(self, load: float):
        """Use the calculated solution to return the power output per plant to reach the load"""
        # we know the plants are sorted in reverse cost / MW, so we need to turn the lowest ones to the max, if the
        # solution determined that they needed to be switched on
        configuration = [0.0 for _ in self.plants]
        power = 0
        for i, (p, s) in enumerate(zip(self.plants, self.status)):
            if not s:
                continue
            if power + p.pmax < load:
                configuration[i] = p.pmax
                power += p.pmax
            else:
                configuration[i] = load - power
                return configuration
        raise AssertionError("solution was not valid!")


def _calculate_effective_pminmax(plants: List[Plant], fuels: Dict[str, Fuel]) -> Iterable[Plant]:
    """Corrections to the pmin / pmax of each plant according to fuel factor"""
    for p in plants:
        calculated = dataclasses.replace(p,
                                         pmin=p.pmin * fuels[p.fuel_type].factor,
                                         pmax=p.pmax * fuels[p.fuel_type].factor)
        if p.fuel_type == "wind":
            # for wind we consider they always output their pmax when they are switched on
            calculated.pmin = calculated.pmax
        yield calculated


def _solve_dfs(load, plants, solution: Solution, i=0):
    # consider the solution space as a tree, sorted by cost / MW (the nodes on the higher branches have the highest
    # cost) so we want to turn on the plants represented by nodes on the lowest branch first, and only turn them off if
    # this does not yield a solution.
    if i == len(plants):
        return solution.is_solution(load)
    if not solution.can_solve(load):
        # shortcut if the solution is not possible
        return False
    # start exploring the right branch, since it is cheaper
    solution.add(i)
    if _solve_dfs(load, plants, solution, i + 1):
        return True
    # ok, didn't work, start exploring the left branch
    solution.remove(i)
    if _solve_dfs(load, plants, solution, i + 1):
        return True
    return False


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
