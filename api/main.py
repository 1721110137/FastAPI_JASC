from fastapi import FastAPI
import sqlite3
from typing import List
from pydantic import BaseModel
from pydantic import EmailStr
from fastapi import HTTPException
from fastapi import status

class Mensaje (BaseModel):
    mensaje: str

class Contactos (BaseModel):
    id_contacto: int
    nombre: str
    email: EmailStr
    telefono: str

class ContactosIN (BaseModel):
    nombre: str
    email: str
    telefono: str

description = """
    #Contactos API REST
    Api para crear un CRUD
    de la tabla contactos
    """

app = FastAPI(
    title = "Contactos API REST",
    description = description,
    version = "0.0.1",
    terms_of_serice="http://example.com/terms/",
    contact = {
    "name" : "Alfredo Cuellar",
    "email" : "1721110137@utectulancingo.edu.mx",
    "url": "https://github.com/1721110137"
    }
)

@app.get(
    "/",
    response_model = Mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Endpoint principal",
    description = "Regresa un mensaje de Bienvenida"
)

async def read_root():
    response = {"mensaje" : "Hola"}
    return response

@app.get(
    "/contactos/{id_contacto}",
    response_model = List[Contactos],
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Lista de contactos",
    description = "Endpoint que regresa un array con todos los contactos"
)

async def read_root():
    response = {"mensaje" : "Contactos"}
    return response

async def get_contactos():
    try:
        with sqlite3.connect("api/sql/contactos.db") as connection:
            connection.row_factory = sqlite3.Row()
            cursor = connection.cursor()
            cursor.execute("SELECT id_contacto, nombre, email, telefono FROM contactos;")
            response = cursor.fetchall() ## Fetchall devuelve un arreglo
            return response
    
    except Exception as error:
        print(f"Error en get_contactos{error.args}")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Error al consultar los datos"
        )
