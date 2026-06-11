.PHONY: up down build test lint logs db-shell redis-shell clean

up:                    ## Start all services
	docker-compose up -d

down:                  ## Stop all services
	docker-compose down

build:                 ## Build all images
	docker-compose build

test:                  ## Run tests
	pytest tests/ backend/tests/ -v

lint:                  ## Code linting
	ruff check .
	black --check .

logs:                  ## View backend logs
	docker-compose logs -f backend

db-shell:              ## Enter PostgreSQL shell
	docker-compose exec db psql -U postgres debate_agent

redis-shell:           ## Enter Redis CLI
	docker-compose exec redis redis-cli

clean:                 ## Remove all containers and volumes
	docker-compose down -v

dev-backend:           ## Start backend in dev mode
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:          ## Start frontend in dev mode
	cd frontend && npm start
