all: setup test build

setup:
	poetry install

test:
	poetry run pytest

run:
	# run locally (for development)
	poetry run uvicorn --port 8888 --reload powerplant.app:app

build:
	docker build -t power_challenge .

up: build
	# run docker image
	docker run --rm -p 8888:8000 power_challenge
