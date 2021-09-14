# FROM python:3.6

# pull official base image
FROM python:3.6.9-alpine

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt
# copy project
COPY ./* /usr/src/app
# TODO: 
COPY . /


# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip


EXPOSE 8000

CMD uvicorn app.server.app:app --host 0.0.0.0 --port=8000
