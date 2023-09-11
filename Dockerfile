FROM python:3.7.4-alpine3.10

# Install libffi-dev
RUN apk add --no-cache libffi-dev

# Copy requirements.txt and install packages
ADD ./requirements.txt /app/requirements.txt

RUN apk update && apk add --no-cache postgresql-dev

RUN set -ex \
    && apk add --no-cache --virtual .build-deps postgresql-dev build-base \
    && apk add --no-cache zlib-dev libjpeg-turbo-dev


RUN set -ex \
    && apk add --no-cache --virtual .build-deps postgresql-dev build-base \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt \
    && /env/bin/pip install gunicorn \
    && /env/bin/pip install psycopg2-binary \
    && /env/bin/pip install psycopg2 \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps

# Copy the rest of the application code
ADD . /app
WORKDIR /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "space_djangov3.wsgi"]