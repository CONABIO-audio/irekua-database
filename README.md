# Irekua-database

This set of Django apps define the core Irekua data models.


# Start developing

## Develop with Docker and Docker-compose

The easiest way of building a development environment is with docker and
docker-compose. Please follow the next steps to start developing with docker:

### Build the image

Please run

    sudo docker-compose build

### Initialize the database

Check that the datase is setup and responding:

    sudo docker-compose run app python manage.py check

Make the initial migration by running:

    sudo docker-compose run app python manage.py migrate

Create a superuser:

    sudo docker-compose run app python manage.py createsuperuser

### Start the development servers

To start the development apps run:

    sudo docker-compose up

### Navigate to the admin app

The database admin is at:

    localhost:5002/admin

### Run the tests

To run the test suite:

    sudo docker-compose run app python manage.py test --keepdb
