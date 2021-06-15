.PHONY: build check migrate createsuperuser up test

build:
	docker-compose build

check:
	docker-compose run app python manage.py check

migrate:
	docker-compose run app python manage.py migrate

createsuperuser:
	docker-compose run app python manage.py createsuperuser

up:
	docker-compose up

test: build
	docker-compose run app pytest

clean: clean-build clean-pyc clean-test clean-cache

clean-cache:
	rm -fr .mypy_cache
	rm -fr .pytest_cache

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
