from fastapi import FastAPI, Request
import json
import os
from typing import List
import psycopg2

app = FastAPI()


# FUNCIÓN DE LEER LAS NOTAS 
def leer_notas() -> List[str]:
    try:
        with open("data/notas.txt", "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        return []
# FUNCIÓN DE GUARDAR LAS NOTAS
def guardar_nota(contenido: str):
    with open("data/notas.txt", "a", encoding="utf-8") as f:
        f.write(contenido + "\n")

#Conexión con PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "notas_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notas (
            id SERIAL PRIMARY KEY,
            contenido TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

#Crear tabla al iniciar
init_db()


#ENDPOINTS
@app.get("/")
async def root():
    return {
        "message": "Welcome to the FastAPI application! "
        "You can use this API to manage your notes."
    }

#GET DE VER LAS NOTAS
@app.get("/notes")
async def get_notes():

    # TODO: Implementar
    return {"notes": leer_notas()}

#POST DE GUARDAR NOTAS
@app.post("/notes")
async def create_note(contenido: str):
    guardar_nota(contenido)

    #Guardar nota en DB
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notas (contenido) VALUES (%s)", (contenido,))
    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Note created successfully!", "note": contenido}

#GET DE CONTAR NOTAS
@app.get("/conteo")
async def conteo_notas():
    notas = leer_notas()
    return {"total_notas": len(notas)}

@app.get("/autor")
async def get_autor():
    autor = os.getenv("AUTOR","Autor no configurado")
    return {"autor": autor}

#GET DE LEER NOTAS DESDE DB
@app.get("/notas-db")
async def get_notes_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, contenido FROM notas")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {"notas_db": [{"id": r[0], "contenido": r[1]} for r in rows]}