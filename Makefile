.PHONY: up down build logs restart clean

up:
	docker compose up --build -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

restart:
	docker compose down && docker compose up --build -d

clean:
	docker compose down -v
