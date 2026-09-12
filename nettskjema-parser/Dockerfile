FROM python:3.14.7-alpine3.24

RUN apk update
RUN apk add curl

WORKDIR /parser
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

CMD ["python3", "./src/main.py"]