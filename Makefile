install:
	@poetry install

test:
	poetry run pytest -vv tests/ --cov=gendiff --cov-report xml

lint:
	poetry run flake8 page-loader

check: test lint

build: check
	@poetry build

.PHONY: install test check lint build
