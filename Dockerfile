FROM python:3.8-alpine
LABEL maintainer='Daniele Mancuso'

ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:${PATH}"

RUN pip install --upgrade pip

COPY requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev \
      python3-dev libffi libffi-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /api
WORKDIR /api
COPY sample_auth_api /api
COPY scripts /scripts
RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D api_service
RUN chown -R api_service:api_service /vol/
RUN chmod -R 755 /vol/web
USER api_service

CMD ["entrypoint.sh"]

