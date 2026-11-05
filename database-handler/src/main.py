from fastapi import FastAPI
import psycopg2
import socket

registered_adresses = [
    "discord_bot",
]

app = FastAPI()
conn = psycopg2.connect(dbname='template1', user='postgres', host='peter_db', password='postgres')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

@app.post("/trigger_update")
def set_stuff():
    acc = []
    for addr in registered_adresses:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((addr, 69420))
            s.sendall(b"Update Time")
            data = s.recv(1024)
            acc.append({addr: data.decode("utf-8")})

    return acc

