# Hello There

## how to run frontend:
`> npm install`

`> npm start`

## how to run api server
`> ./manage.py runserver`

## how to  run core
`> sudo python runcore.py`

## how to run critical tests
note that critical test can  only be run in docker

`> sudo python runtests_critical.py`

## how to run docker
`> docker run --cap-add=NET_ADMIN -p 8124:8000 psec:debug`

docker is listenging for http requests on localhost:8124