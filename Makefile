.PHONY: build check migrate createsuperuser up test

build:
	sudo docker-compose build

check:
	sudo docker-compose run app python manage.py check

migrate:
	sudo docker-compose run app python manage.py migrate

createsuperuser:
	sudo docker-compose run app python manage.py createsuperuser

up:
	sudo docker-compose up

test: build
	sudo docker-compose run app python manage.py test --keepdb
