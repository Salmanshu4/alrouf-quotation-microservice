.PHONY: help install test run docker-build docker-run clean

help: ## Show this help message
	@echo "Alrouf Quotation Microservice - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install pytest-cov black flake8

test: ## Run tests with pytest
	pytest -v

test-cov: ## Run tests with coverage report
	pytest --cov=main --cov-report=html --cov-report=term

test-watch: ## Run tests in watch mode
	pytest-watch

run: ## Run the service locally
	python main.py

run-dev: ## Run the service with auto-reload
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

docker-build: ## Build Docker image
	docker build -t alrouf-quotation-service .

docker-run: ## Run Docker container
	docker run -p 8000:8000 alrouf-quotation-service

docker-compose-up: ## Start services with docker-compose
	docker-compose up --build

docker-compose-down: ## Stop docker-compose services
	docker-compose down

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

format: ## Format code with black
	black main.py test_main.py test_service.py

lint: ## Run linting with flake8
	flake8 main.py test_main.py test_service.py

check: ## Run all checks (format, lint, test)
	@echo "Running code formatting..."
	@make format
	@echo "Running linting..."
	@make lint
	@echo "Running tests..."
	@make test

demo: ## Run the demo test script
	python test_service.py

setup: ## Complete setup for development
	@echo "Setting up development environment..."
	@make install-dev
	@echo "Development environment ready!"
	@echo "Run 'make run-dev' to start the service"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make demo' to test the API"

all: clean install test ## Clean, install, and test
