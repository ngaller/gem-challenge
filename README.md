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

    poetry run src/app.py

### Running the Tests

    poetry run pytest

### Deploy Using Docker

    docker build .

## Solution Architecture


