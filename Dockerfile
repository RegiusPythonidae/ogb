# pull official base image
FROM nickgryg/alpine-pandas

MAINTAINER Temur Chichua "temur.chichua@iliauni.edu.ge"

# set work directory
WORKDIR .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV FLASK_ENV=production \
    FLASK_APP=autoapp

ENV GROUP_ID=1000 \
    USER_ID=1000

# install dependencies
RUN python -m pip install -U --force-reinstall pip
RUN apk update
RUN apk add --virtual build-deps build-base gcc musl-dev jpeg-dev zlib-dev
RUN apk add postgresql-dev
RUN rm -rf /var/cache/apk/*

# COPY soruce > destination
COPY ./requirements/prod.txt ./requirements/prod.txt
RUN pip install gunicorn
RUN pip install -r ./requirements/prod.txt
# copy project
COPY . .

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh

RUN chown www:www -R /src
RUN chmod +x /src

EXPOSE 5000

USER www

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "--timeout", "200", "manage"]
# docker build --tag local-app .
# docker run -p 5000:5000 -t -i local-app:latest

#/dedaenabar/static/uploads/profile_pictures > /root/images