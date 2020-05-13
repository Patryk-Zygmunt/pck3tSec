FROM alpine:latest
RUN apk add python3 && link /usr/bin/python3 /usr/bin/python && link /usr/bin/pip3 /usr/bin/pip
RUN python -m pip install --upgrade pip
RUN apk add iptables gcc libc-dev python3-dev libffi-dev libxml2-dev libxslt-dev
COPY ./requirements.txt /app/requirements.txt
RUN pip install wheel
RUN pip install  -r app/requirements.txt
# remove packages that were only needed for compiling python packages
RUN apk del gcc libc-dev python3-dev libffi-dev libxml2-dev libxslt-dev
COPY ./ /app
WORKDIR app
CMD api/manage.py runserver 0.0.0.0:8000 & ./runcore.py eth0
# api/manage.py runserver 0.0.0.0:8000