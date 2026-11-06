FROM python:3.14.7-alpine3.24

RUN apk update
RUN apk add \
    build-base \
    libpq-dev \
    postgresql-client \
    curl

WORKDIR /handler
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

CMD ["fastapi", "run", "./src/main.py"]