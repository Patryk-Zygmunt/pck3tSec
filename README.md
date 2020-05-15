# Hello There
![Basci Tests](https://github.com/Matshec/pck3tSec/workflows/Basci%20Tests/badge.svg)

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
```
 docker  network create nazwa-sieci
 docker run --network nazwa-sieci -p 81:80  patrykzygmunt/pck3tsec-ui
 docker run --cap-add=NET_ADMIN --name backend --network nazwa-sieci  -p 8123:8000 matshec/psec-hub:latest
```

docker is listening for http requests on localhost:8124
