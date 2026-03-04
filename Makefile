# Makefile
# Shortcuts for common operations. Run 'make help' to see all.

.PHONY: help up down db-shell migrate seed test lint format

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up:  ## Start all services
	docker compose -f infra/docker/docker-compose.yml up -d

down:  ## Stop all services
	docker compose -f infra/docker/docker-compose.yml down

db-shell:  ## Open PostgreSQL shell
	docker exec -it dailyreport-db psql -U dailyreport -d dailyreport

migrate:  ## Run database migrations
	alembic upgrade head

migrate-new:  ## Generate new migration (usage: make migrate-new msg="add xyz")
	alembic revision --autogenerate -m "$(msg)"

seed:  ## Seed database with initial data
	uv run python scripts/seed.py

test:  ## Run all tests
	uv run pytest tests/ -v

test-unit:  ## Run unit tests only
	uv run pytest tests/unit/ -v

lint:  ## Run linter
	uv run ruff check src/ tests/

format:  ## Format code
	uv run ruff format src/ tests/

typecheck:  ## Run type checker
	uv run mypy src/daily_report/
