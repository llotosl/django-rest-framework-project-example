
# pull official base image
FROM python:3.10.9-alpine

RUN apk update && apk add python3-dev gcc libc-dev libffi-dev

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install gunicorn
ADD ./backend/requirements/common.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD ./backend /app/backend
ADD ./docker /app/docker

RUN chmod +x /app/docker/backend/server-entrypoint.sh
RUN chmod +x /app/docker/backend/worker-entrypoint.sh

