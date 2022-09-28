from fastapi import FastAPI
import sqlite3
from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status

class mensaje (BaseModel):
    mensaje: str()

class contactos (BaseModel):
    id_contacto: int()
    nombre: str()
    email: str()
    telefono: str()

class contactosIN (BaseModel):
    nombre: str()
    email: str()
    telefono: str()

description: """
    #Contactos API REST
    Api para crear un CRUD
    de la tabla contactos
    """

app = FastAPI(
    title = "Contactos API REST",
    description = description,
    version = "0.1",
    contact = {"name" : "Alfredo Cuellar",
    "email" : "1721110137@utectulancingo.edu.mx"}
)

@app.get(
    "/",
    response_model = mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Endpoint principal",
    description = "Regresa un mensaje de Bienvenida"
)

async def read_root():
    response = {"mensaje" : "version 0.1"}
    return response

@app.get(
    "/contactos/",
    response_model = List [contactos],
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Lista de contactos",
    description = "Endpoint que regresa un array con todos los contactos"
)

async def get_contactos():
    try:
        with sqlite3.connect("api/sql/contactos.db") as connection:
            connection.row_factory = sqlite3.Row()
            cursor = connection.cursor()
            cursor.execute("SELECT id_contacto, nombre, email, telefono FROM contactos;")
            response = cursor.fetchall()
            return response
    
    except Exception as error:
        print(f"Error en get_contactos {error.args}")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Error al consultar los datos"
        )
