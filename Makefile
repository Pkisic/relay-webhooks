.DEFAULT_GOAL := help

# Run every task inside the project environment and fail if uv.lock is stale,
# so local runs behave like CI and Docker builds.
UV_RUN := uv run --locked

HOST ?= 127.0.0.1
PORT ?= 8000

.PHONY: help install dev lint format format-check typecheck test check build

# The quality gate must run its steps in order, even under `make -j`.
.NOTPARALLEL:

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*## "} {printf "  %-14s %s\n", $$1, $$2}'

## Setup

install: ## Install locked dependencies
	uv sync --locked

build: ## Build the package (sdist and wheel)
	uv build

## Development

dev: ## Run the API with auto-reload (override with HOST=... PORT=...)
	$(UV_RUN) uvicorn relay.main:create_app --factory --reload --reload-dir src \
		--host $(HOST) --port $(PORT)

## Quality

lint: ## Lint with ruff
	$(UV_RUN) ruff check .

format: ## Format code and apply safe lint fixes
	$(UV_RUN) ruff format .
	$(UV_RUN) ruff check --fix .

format-check: ## Verify formatting without changing files
	$(UV_RUN) ruff format --check .

typecheck: ## Type-check with mypy
	$(UV_RUN) mypy src tests

test: ## Run the test suite
	$(UV_RUN) pytest

check: lint format-check typecheck test ## Run the full quality gate (used by CI)
