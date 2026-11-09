FROM python:3.14.7-alpine3.24

RUN apk update
RUN apk add curl

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./src .

CMD ["python3", "./main.py"]