# Makefile
.PHONY: checks format

help:
	@echo "checks - Runs isort/black/flake8/mypy"
	@echo "format" - Runs isort/black format on all files

checks:
	poetry run isort --diff .
	poetry run black --check .
	poetry run flake8
	poetry run mypy

format:
	poetry run isort .
	poetry run black .