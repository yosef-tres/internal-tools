# FDC (Fast & Dirty Commit) Makefile
# 
# This Makefile provides shortcuts for common development tasks
# using UV as the Python package manager.

.PHONY: help install start test clean migrate-new migrate-up migrate-down migrate-history migrate-current

help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies with UV"
	@echo "  make start          - Start the Streamlit application"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Clean up cache files and directories"
	@echo "  make migrate-new    - Create new migration (usage: make migrate-new m='migration message')"
	@echo "  make migrate-up     - Upgrade database to latest version"
	@echo "  make migrate-down   - Downgrade database by one version"
	@echo "  make migrate-history - Show migration history"
	@echo "  make migrate-current - Show current migration version"

install:
	uv pip install -e .

start:
	uv run streamlit run fdc/app.py

test:
	uv run pytest

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.egg-info
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Migration commands using UV
migrate-new:
	@if [ -z "$(m)" ]; then \
		echo "Error: Migration message required. Usage: make migrate-new m='migration message'"; \
		exit 1; \
	fi
	uv run migrate-new "$(m)"

migrate-up:
	uv run migrate-up

migrate-down:
	uv run migrate-down

migrate-history:
	uv run migrate-history

migrate-current:
	uv run migrate-current
