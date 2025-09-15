from fastapi import FastAPI, Request
import json
import os
from typing import List

app = FastAPI()

def leer_notas() -> List[str]:
    try:
        with open("data/notas.txt", "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []

def guardar_nota(contenido: str):
    with open("data/notas.txt", "a", encoding="utf-8") as f:
        f.write(contenido + "\n")

@app.get("/")
async def root():
    return {
        "message": "Welcome to the FastAPI application! "
        "You can use this API to manage your notes."
    }


@app.get("/notes")
async def get_notes():

    # TODO: Implementar
    return {"notes": leer_notas()}


@app.post("/notes")
async def create_note(contenido: str):
    guardar_nota(contenido)
    return {"message": "Note created successfully!", "note": contenido}
