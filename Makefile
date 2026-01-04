.PHONY: help build up down restart logs clean test migrate seed

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build all containers
	docker-compose build

up: ## Start all services
	docker-compose up -d

down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

logs: ## Show logs
	docker-compose logs -f

logs-api: ## Show API logs
	docker-compose logs -f api

logs-celery: ## Show Celery logs
	docker-compose logs -f celery_worker celery_beat

clean: ## Clean up containers and volumes
	docker-compose down -v
	docker system prune -f

test: ## Run tests
	docker-compose exec api pytest

test-cov: ## Run tests with coverage
	docker-compose exec api pytest --cov=app --cov-report=html

migrate: ## Run database migrations
	docker-compose exec api alembic upgrade head

migrate-create: ## Create new migration (usage: make migrate-create MSG="message")
	docker-compose exec api alembic revision --autogenerate -m "$(MSG)"

migrate-down: ## Rollback last migration
	docker-compose exec api alembic downgrade -1

seed: ## Seed database with sample data
	docker-compose exec api python scripts/seed_data.py

superuser: ## Create superuser
	docker-compose exec api python scripts/create_superuser.py

shell: ## Open Python shell
	docker-compose exec api python

db-shell: ## Open database shell
	docker-compose exec postgres psql -U portfel -d portfel_db

redis-shell: ## Open Redis CLI
	docker-compose exec redis redis-cli

install-dev: ## Install development dependencies
	cd backend && pip install -e ".[dev]"

format: ## Format code with black and isort
	docker-compose exec api black app/
	docker-compose exec api isort app/

lint: ## Lint code
	docker-compose exec api flake8 app/
	docker-compose exec api mypy app/

backup-db: ## Backup database
	docker-compose exec api python scripts/backup_db.py

dev: ## Start development environment
	docker-compose up -d postgres redis
	cd backend && uvicorn app.main:app --reload

prod-build: ## Build for production
	docker-compose -f docker-compose.prod.yml build

prod-up: ## Start production environment
	docker-compose -f docker-compose.prod.yml up -d

prod-down: ## Stop production environment
	docker-compose -f docker-compose.prod.yml down
