## Makefile for Pipegram Flask API
##
## This Makefile defines shortcuts for common tasks. Each command
## must be indented with a TAB character (\t). Do not replace the
## leading TABs with spaces or the GNU Make parser will error with
## “missing separator”.

.PHONY: install run test build compose-up clean

## Create a virtual environment and install dependencies
install:
	python -m venv .venv && \
	. .venv/Scripts/activate && \
	pip install -r requirements.txt

## Run the application using the built‑in Flask server (development only)
run:
	python run.py

## Run the test suite with pytest
test:
	pytest -x -s

## Build the Docker image
build:
	docker build -t pipegram-flask .

## Bring up the application using Docker Compose.
## This rule assumes Docker Compose V2 syntax (`docker compose`).
## If your environment only has the older `docker-compose`, run that
## command manually instead of using this target.
compose-up:
	docker compose up --build

## Remove the local virtual environment
clean:
	rmdir /S /Q .venv