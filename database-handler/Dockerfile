FROM python:3.14.7-alpine3.24

RUN apk update
RUN apk add \
    build-base \
    libpq-dev \
    postgresql-client \
    curl

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./src .

CMD ["fastapi", "run", "./main.py"]