FROM alpine:latest
RUN apk add python3
RUN link /usr/bin/python3 /usr/bin/python && link /usr/bin/pip3 /usr/bin/pip
RUN python -m pip install --upgrade pip
RUN apk add iptables gcc libc-dev python3-dev libffi-dev libxml2-dev libxslt-dev
COPY ./ /app
RUN pip install wheel
RUN pip install  -r app/requirements.txt
RUN apk del gcc libc-dev python3-dev libffi-dev libxml2-dev libxslt-dev
