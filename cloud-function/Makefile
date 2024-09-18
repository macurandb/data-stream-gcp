.PHONY: all clean test docs

# existing VIRTUAL_ENV might mess with poetry, so make sure it is gone
VIRTUAL_ENV=
unexport VIRTUAL_ENV

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9._-]+:.*?## / {printf "\033[1m\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

test: ## Run pytest
	poetry run pytest -rA -vvs -s --log-level INFO

cov: ## Run coverage
	poetry run pytest --cov=src tests

install: ## Install dependencies and the package to poetry venv
	poetry install

lint: ## Run mypy and flake8 to check the code
	poetry run mypy src tests
	poetry run flake8 src tests
	poetry run ruff check src tests
	$(MAKE) pylint

fmt: ## Run black to format the code
	poetry run black src tests

test_envs: ## Run to test in many envs
	poetry run tox -p -- -v -s

docs: ## Generate HTML documentation using Sphinx
	@echo "Forcing documentation rebuild..."
	poetry run sphinx-build -b html docs/source docs/build/html
	@touch docs/build/html/index.html
