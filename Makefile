.PHONY: install run test build compose-up clean

# Create virtual environment and install dependencies
install:
	python3 -m venv .venv && \
	. .venv/bin/activate && \
	pip install -r requirements.txt

# Run the application using the built‑in server (development only)
run:
	python run.py

# Run the test suite with pytest
test:
	pytest -x -s

# Build the Docker image
build:
	docker build -t pipegram-flask .

# Bring up the application with docker-compose
compose-up:
    # Use the new `docker compose` (space) syntax; fall back to `docker-compose` if needed.
    @if command -v docker compose >/dev/null 2>&1; then \
      docker compose up --build; \
    else \
      docker-compose up --build; \
    fi

# Remove virtual environment
clean:
	rm -rf .venv