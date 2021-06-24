.PHONY: build check migrate createsuperuser up test

codecov_token = 39e4b593-e752-48fc-a92f-a18717fc48c1

module = irekua_geo

build:
	docker-compose build

check:
	docker-compose run app python manage.py check

migrate:
	docker-compose run app python manage.py migrate

createsuperuser:
	docker-compose run app python manage.py createsuperuser

clean: clean-build clean-pyc clean-test clean-cache

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-cache:
	rm -fr .mypy_cache
	rm -fr .pytest_cache

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

coverage:
	docker-compose run app pytest && \
	docker-compose run app codecov --token=${codecov_token}

up:
	docker-compose up --detach

test:
	docker-compose run app pytest