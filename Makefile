.PHONY: help install dev test lint format clean docker-up docker-down docker-build docker-push

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

dev: ## Start development environment
	docker-compose up -d

test: ## Run tests
	pytest backend/tests/ -v --cov=backend --cov-report=html

lint: ## Run linting checks
	black --check backend/
	isort --check-only backend/
	flake8 backend/
	mypy backend/

format: ## Format code
	black backend/
	isort backend/

clean: ## Clean up temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/ .mypy_cache/ .pytest_cache/

docker-up: ## Start Docker services
	docker-compose up -d

docker-down: ## Stop Docker services
	docker-compose down

docker-build: ## Build Docker images
	docker-compose build

docker-push: ## Push Docker images to registry
	docker push $(DOCKER_USERNAME)/istock-backend:latest
	docker push $(DOCKER_USERNAME)/istock-frontend:latest

migrate: ## Run database migrations
	cd backend && alembic upgrade head

migrate-create: ## Create new migration
	cd backend && alembic revision --autogenerate -m "$(message)"

seed: ## Seed database with sample data
	cd backend && python scripts/seed_data.py

logs: ## View logs
	docker-compose logs -f

shell: ## Open shell in backend container
	docker-compose exec backend bash

db-shell: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U mystock_user -d mystock_ai

redis-cli: ## Open Redis CLI
	docker-compose exec redis redis-cli

flower: ## Open Flower dashboard
	open http://localhost:5555

docs: ## Open API documentation
	open http://localhost:8000/docs

frontend: ## Open frontend
	open http://localhost:3000

health: ## Check service health
	curl http://localhost:8000/health

production-up: ## Start production environment
	docker-compose -f docker-compose.prod.yml up -d

production-down: ## Stop production environment
	docker-compose -f docker-compose.prod.yml down

production-logs: ## View production logs
	docker-compose -f docker-compose.prod.yml logs -f

monitoring: ## Open monitoring dashboards
	open http://localhost:9090  # Prometheus
	open http://localhost:3001  # Grafana