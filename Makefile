# Makefile for Kyoryoku project

.PHONY: help install dev test format lint clean docker-up docker-down backend-dev frontend-dev

help:
	@echo "Available commands:"
	@echo "  install       Install all dependencies"
	@echo "  dev          Run both backend and frontend in development mode"
	@echo "  test         Run tests"
	@echo "  format       Format code with black"
	@echo "  lint         Run linting checks"
	@echo "  clean        Clean up generated files"
	@echo "  docker-up    Start Docker containers"
	@echo "  docker-down  Stop Docker containers"

install:
	cd backend && pip3 install -r requirements.txt
	cd frontend && npm install

backend-dev:
	cd backend && uvicorn app.main:app --reload --port 8000

frontend-dev:
	cd frontend && npm run dev

dev:
	@echo "Starting development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@make -j 2 backend-dev frontend-dev

test:
	cd backend && pytest

format:
	cd backend && black app tests

lint:
	cd backend && flake8 app tests
	cd backend && mypy app

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf backend/.coverage
	rm -rf backend/htmlcov
	rm -rf backend/.pytest_cache
	rm -rf frontend/node_modules
	rm -rf frontend/dist

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

migrate:
	cd backend && alembic upgrade head

migration:
	cd backend && alembic revision --autogenerate -m "$(message)"