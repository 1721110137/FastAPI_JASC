from fastapi import FastAPI, Query
import sqlite3
from typing import List
from pydantic import BaseModel
from pydantic import EmailStr
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse

class Mensaje(BaseModel):
    mensaje: str

class Contacto(BaseModel):
    id_contacto: int
    nombre: str
    email: EmailStr
    telefono: str

class ContactoIN(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str

description = """
API_REST para realizar un CRUD en la base de datos "Contactos".
    """

app = FastAPI(
    title = "Contactos API REST",
    description = description,
    version = "0.0.1",
    terms_of_serice="http://example.com/terms/",
    contact = {
    "name" : "José Alfredo Sorcia Cuellar",
    "email" : "1721110137@utectulancingo.edu.mx",
    "url": "https://github.com/1721110137"
    }
)
## API mensaje de que funciona-------------------------------------------------------------------------------------------- ##
@app.get(
    "/",
    response_model = Mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Endpoint principal.",
    description = "Regresa un mensaje indicando el correcto funcionamiento del endpoint."
)

async def read_root():
    response = {"mensaje" : "EL endpoint funciona correctamente."}
    return response

## EP consulta de todos los datos---------------------------------------------------------------------------------------- ##
@app.get(
    "/contactos/",
    response_model = List[Contacto],
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Endpoint lista de contactos.",
    description = "Regresa un arreglo con todos los contactos de la base de datos."
)

async def get_contactos():
    try:
        with sqlite3.connect("api/sql/contactos.db") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("SELECT id_contacto, nombre, email, telefono FROM contactos;")
            response = cursor.fetchall()
            return response
    
    except Exception as error:
        print(f"Error en get_contactos{error.args}")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Error al consultar los contactos de la base de datos"
        )

## EP consulta por ID---------------------------------------------------------------------------------------------------- ##
@app.get(
    "/contactos/{id_contacto}",
    response_model = Contacto,
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Devuelve todos los datos de un contacto",
    description = "Endpoint para consultar por id_contacto"
)

async def get_contacto_id(id_contacto: int):
    try:
        with sqlite3.connect("api/sql/contactos.db") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            query=("SELECT id_contacto, nombre, email, telefono FROM contactos WHERE id_contacto= ?;")
            values=(id_contacto,)
            cursor.execute(query,values)
            response = cursor.fetchone()
            if response == None:
                return JSONResponse(status_code = 404, content = {"mensaje" : "El id_contacto es inexistente."})
            else:
                return response

    except Exception as error:
        print(f"Error en get_contacto_id{error.args}")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Error al consultar el ID"
)

## EP inertar nuevo registro--------------------------------------------------------------------------------------------- ##
@app.post(
   "/contactos/",
    response_model = Mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Insertar un nuevo registro",
    description = "Endpoint para ingresar un nuevo registro"
)

def post_contacto(contacto:ContactoIN):
    print(f"Nombre:{contacto.nombre}")

    try:
        with sqlite3.connect("api/sql/contactos.db") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            query="INSERT INTO contactos (nombre, email, telefono) VALUES (?, ?, ?);"
            values=(contacto.nombre, contacto.email, contacto.telefono)
            cursor.execute(query,values)
            response = {"mensaje": "Contacto registrado con exito."}
            return response

    except Exception as error:
        print(f"Error al ingresar un nuevo contacto{error.args}")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Error al insertar registro"
)

## EP actualizar un registro--------------------------------------------------------------------------------------------- ##
@app.put(
    "/contactos/{id_contacto}",
    response_model = Mensaje,
    summary ="Actualiza un contacto existente",
    description = "Endpoint para actualizar un contacto"
)
async def put_contacto(id_contacto: int, contacto: ContactoIN):
    try:
        with sqlite3.connect("api/sql/contactos.db") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            query = "SELECT * FROM contactos WHERE id_contacto = ?;"
            values = (id_contacto,)
            cursor.execute(query, values)
            response = cursor.fetchone()
            if response == None:
                return JSONResponse(status_code = 404, content = {"mensaje" : "El id_contacto es inexistente."})
            else:
              query = "SELECT email FROM contactos where email = ?;"
              email = (contacto.email,)
              cursor.execute(query, email)
              result = cursor.fetchone()

              if result == None:
                query="UPDATE contactos SET nombre= ?, email= ?, telefono= ? WHERE id_contacto = ?;"
                values = (contacto.nombre, contacto.email, contacto.telefono, id_contacto)
                cursor.execute(query, values)
                response = {"mensaje":"Contacto actualizado con éxito"}
                return response
              else:
                return JSONResponse(status_code = 404, content = {"mensaje" : "El email ya existe, ingrese uno diferente"})

    except Exception as error:
        print(f"Error al consultar datos{error.args}")
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el contacto"
        )


## EP eliminar un registro----------------------------------------------------------------------------------------------- ##
@app.delete(
    "/contactos/{id_contacto}",
    response_model = Mensaje,
    status_code = status.HTTP_202_ACCEPTED,
    summary = "Elimina un contacto existente",
    description = "Endpoint para eliminar un contacto por ID"
)
async def delete_contacto(id_contacto:int): 
  try:
    with sqlite3.connect ("api/sql/contactos.db") as connection:
      connection.row_factory = sqlite3.Row
      cursor = connection.cursor()
      query = "SELECT id_contacto, nombre, email, telefono FROM contactos WHERE id_contacto = ?;"
      values = (id_contacto,)
      cursor.execute(query, values)
      response = cursor.fetchone()
      if response == None:
        return JSONResponse(status_code = 404, content = {"mensaje":"El id_contacto es inexistente."}) 
      else:  
        query = "DELETE FROM contactos WHERE id_contacto = ?;"
        values = (id_contacto,)
        cursor.execute(query, values)
        response = {"mensaje":"Contacto eliminado con éxito"}
        return response
  except Exception as error:
    print(f"Error al eliminar el contacto{error.args}")
    raise HTTPException(
      status_code = status.HTTP_400_BAD_REQUEST,
      detail = "Error al eliminar un contacto"
    )
