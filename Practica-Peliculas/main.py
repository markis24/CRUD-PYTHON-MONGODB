from fastapi import FastAPI
from fastapi import HTTPException

from db import filmsDB

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/films")
def get_all_films():
    # Llama a la función `read` de la clase `filmsDB` para obtener todas las películas
    data = filmsDB.read()

    # Si no se encontraron películas en la base de datos, levanta una excepción 404
    if data is None:
        raise HTTPException(status_code=404, detail="No se encontraron películas en la base de datos")

    # Devuelve todas las películas como respuesta
    return {"data": data}


@app.get("/films/{id}")
def get_film_by_id(id: str):
    # Llamamos a la función `read_by_id` de la clase `filmsDB` para obtener la película por su ID
    data = filmsDB.read_by_id(id)

    # Si no se encontró ninguna película con el ID proporcionado, levantamos una excepción 404
    if data is None:
        raise HTTPException(status_code=404, detail=f"No se encontró la película con el ID {id}")

    # Si se encontró la película, la devolvemos como respuesta
    return {"data": data}


@app.delete("/films/{id}")
def delete_by_id(id: str):
    # Llama a la función `delete_by_id` de la clase `filmsDB` para eliminar la película por su ID
    deleted_count = filmsDB.delete_by_id(id)

    # Si no se eliminó ninguna película, levanta una excepción 404
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"No se encontró ninguna película con el ID {id}")

    # Devuelve un mensaje de éxito si la película se eliminó correctamente
    return {"message": f"Se eliminó correctamente la película con el ID {id}"}


@app.post("/films/")
def create_film(film_data: dict):
    try:
        film_id = filmsDB.create_film(film_data)  # Llama a la función create_film del módulo filmsDB
        if film_id:
            return {"message": f"Película creada con éxito. ID: {film_id}"}
        else:
            raise HTTPException(status_code=500, detail="Error al crear la película en la base de datos")
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al crear la película: {e}")


@app.put("/films/{id}")
def create_film(film_data: dict):
    try:
        film_id = filmsDB.update_film(film_data)  # Llama a la función create_film del módulo filmsDB
        if film_id:
            return {"message": f"Película creada con éxito. ID: {film_id}"}
        else:
            raise HTTPException(status_code=500, detail="Error al crear la película en la base de datos")
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno al crear la película: {e}")
