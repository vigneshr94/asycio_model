APP_DIR := src
SERVER_DIR := src/app
TEST_DIR := tests
CONFIG_FILE := src/config.json
APP_MODULE := app
APP_NAME := app
HOST := "0.0.0.0"
PORT := 8080
MOD ?= dummy.py

.PHONY: all
all: help

.PHONY: run
run: install.stamp
	@echo "Running the $(MOD)"
	@poetry run python3 $(MOD)

install.stamp: pyproject.toml poetry.lock
	@echo "Running poetry install"
	@poetry lock --no-update
	@poetry install
	@touch install.stamp

.PHONY: test
test: install.stamp
	@echo "Running pytest"
	@poetry run pytest $(TEST_DIR)

.PHONY: lint
lint:
	@echo "Running flake8 linter"
	@poetry run flake8 $(APP_DIR) $(TEST_DIR)

.PHONY: format
format:
	@echo "Running black code formatter"
	@poetry run black $(APP_DIR) $(TEST_DIR)

.PHONY: deploy-dev
deploy-dev: install.stamp
	@echo "Deploying the application in development mode"
	@poetry run uvicorn $(APP_MODULE):$(APP_NAME) --app-dir $(SERVER_DIR) --host $(HOST) --port $(PORT) --reload

.PHONY: deploy-prod
deploy-prod: install.stamp
	@echo "Deploying the application in production mode"
	@poetry run uvicorn $(APP_MODULE):$(APP_NAME) --app-dir $(SERVER_DIR) --host $(HOST) --port $(PORT)

.PHONY: update
update:
	@echo "Fetching latest Updates"
	@git fetch
	@echo "Finding differences...."
	@git diff --name-only HEAD origin/$(shell git rev-parse --abbrev-ref HEAD) | grep -E "pyproject.toml|poetry.lock" && (echo "Changes in pyproject.toml or poetry.lock detected. Please run 'make install' to update the dependencies." && exit 1) || echo "No changes in pyproject.toml or poetry.lock detected."
	@echo "Pulling changes...."
	@git pull origin $(shell git rev-parse --abbrev-ref HEAD)

.PHONY: clean
clean:
	@echo "Cleaning cache files...."
	@find . -type d -name '__pycache__' -exec rm -rf {} +

.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  run MOD=<path to module>		Run the passed module"
	@echo "  test         					Run the tests"
	@echo "  lint         					Run the linter"
	@echo "  format       					Run the code formatter"
	@echo "  deploy-dev   					Deploy the application in development mode"
	@echo "  deploy-prod  					Deploy the application in production mode"
	@echo "  update       					Update the application"
	@echo "  help         					Show this help message"
	@echo "  clean        					Remove all generated files"
