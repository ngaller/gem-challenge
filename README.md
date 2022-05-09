# Powerplant Coding Challenge

## About this project

- Implements an algorithm to calculate how much power each of a multitude of different powerplants need to produce
  (a.k.a. the production-plan) when the load is given and taking into account the cost of the underlying energy sources
  (gas, kerosine) and the Pmin and Pmax of each powerplant.
- Expose this algorithm over a REST API

## Usage

### Requirements

For local development you will need the following:

- Python 3.8 or higher (3.8.12 was used during development)
- Poetry

Note that the solution was only tested in a Linux environment.

Install requirements using:

    poetry install

### Running Locally

    poetry run uvicorn --port 8888 --reload powerplant.app:app

Submit a sample payload using:

    curl -X POST localhost:8888 -d @payload1.json --header "Content-Type: application/json"

Access generated API documentation using:

    http://localhost:8888/docs

### Running the Tests

    poetry run pytest

### Deploy Using Docker

    docker build -t power_challenge .
    docker run -p 8888:8000 power_challenge

### Makefile

For convenience a Makefile is provided for the above commands, you may thus use:

    make setup
    make test
    make run
    make build
    make up

## Solution Architecture

The API is implemented in app.py using FastAPI.  The models are defined in

 - `request_models.py`, for the ones provided only as input
 - `models.py`, for the ones used internally or as response
 - `base_models.py`, for the common base

The algorithm is implemented in `solver.py` using a simple tree search where each node represents
the state of a power plant: on or off.  The worst case complexity is thus _O(2^n)_, but there are 2
heuristics that will help the algorithm avoid this case:

 - the plants are sorted in merit order, so that we know normally the first plants in the tree need
   to be turned on
 - the algorithm will stop exploring a branch as soon as it detects that the solution is not
   possible because the minimal load will be above the requirement

Thanks to this, in most cases the algorithm reverts to a greedy search.
