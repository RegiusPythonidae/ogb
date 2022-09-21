# pull official base image
FROM python:3.9.5-alpine

MAINTAINER Temur Chichua "contact@temurchichua.me"

# set work directory
WORKDIR .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV FLASK_ENV=development \
    FLASK_APP=manage

ENV GROUP_ID=1000 \
    USER_ID=1000

# install dependencies
RUN python -m pip install -U --force-reinstall pip
RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev \
#    apk add --virtual build-deps build-base gcc musl-dev jpeg-dev zlib-dev && \
#    apk add postgresql-dev \
    && rm -rf /var/cache/apk/*

COPY ./requirements.txt ./requirements.txt
COPY ./requirements ./requirements

RUN pip install -r requirements.txt
RUN pip install gunicorn
# copy project
COPY . .

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

EXPOSE 5000

USER www

ENTRYPOINT ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "manage"]