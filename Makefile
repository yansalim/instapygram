# Pipegram (Flask) - Unofficial Instagram API
# Makefile for easy Docker management

.PHONY: help start stop restart build logs clean

# Default target
help:
	@echo "Available commands:"
	@echo "  start   - Start the API container"
	@echo "  stop    - Stop the API container"
	@echo "  restart - Restart the API container"
	@echo "  build   - Build the Docker image"
	@echo "  logs    - Show container logs"
	@echo "  clean   - Remove containers and images"

# Start the API
start:
	docker compose up -d

# Stop the API
stop:
	docker compose down

# Restart the API
restart:
	docker compose restart

# Build the Docker image
build:
	docker compose build

# Show logs
logs:
	docker compose logs -f api-instagram

# Clean up containers and images
clean:
	docker compose down --rmi all --volumes --remove-orphans
