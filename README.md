# Locali
A wiki platform for the documentation of locali flora

## Backend

To get a backend service running, make you have docker (docker-machine, docker-compose) installed.

first create/start your docker machine
```
$ docker-machine create -d virtualbox locali
$ eval $(docker-machine env locali)
```

then build up your containers, instatiate them, and run the database migrations
```
$ docker-compose build
$ docker-compose up -d
$ docker-compose run backend alembic upgrade head
```

finally get the machines ip to make calls to it
```
$ docker-machine ip locali
```
