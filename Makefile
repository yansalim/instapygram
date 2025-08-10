.PHONY: up down logs rebuild shell

up:
	docker compose up --build -d

rebuild:
	docker compose build --no-cache
	docker compose up -d

logs:
	docker compose logs -f api-instagram

shell:
	docker compose exec api-instagram /bin/sh || docker compose exec api-instagram /bin/bash

down:
	docker compose down
