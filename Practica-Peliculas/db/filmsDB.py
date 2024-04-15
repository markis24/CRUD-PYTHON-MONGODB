from bson import ObjectId
from fastapi import HTTPException

from db.database import client
from model.films import Film


def read():
    try:
        db = client()  # Llama a la función client() para obtener la base de datos 'cine'
        if db is not None:
            collection = db['films']  # Accede a la colección 'films' de la base de datos 'cine'
            # Obtener todos los documentos de la colección
            result = list(collection.find())

            # Convertir ObjectId a cadenas (strings) para evitar errores de serialización
            for doc in result:
                doc["_id"] = str(doc["_id"])

            return result
        else:
            return None  # Devuelve None si no se pudo conectar a la base de datos
    except Exception as e:
        # Si hay algún otro error al leer los datos, lo capturamos y lo imprimimos
        print(f'Error al leer datos de la base de datos: {e}')
        return None  # Devuelve None si hay un error al leer los datos


def read_by_id(id: str):
    try:
        db = client()  # Llama a la función client() para obtener el cliente de MongoDB
        if db is not None:
            collection = db['films']  # Accede a la colección 'films' de la base de datos 'cine'
            object_id = ObjectId(id)  # Convierte el ID proporcionado a un ObjectId
            result = collection.find_one({'_id': object_id})  # Busca un documento con el ID proporcionado

            # Convertir ObjectId a cadena (string) para evitar problemas de serialización
            if result is not None and '_id' in result:
                result['_id'] = str(result['_id'])

            return result
        else:
            return None  # Devuelve None si no se pudo conectar a la base de datos
    except Exception as e:
        print(f'Error al obtener el documento por ID: {e}')
        return None  # Devuelve None si hay otro error al obtener el documento


def delete_by_id(id: str):
    try:
        db = client()  # Llama a la función client() para obtener el cliente de MongoDB
        if db is not None:
            collection = db['films']  # Accede a la colección 'films' de la base de datos 'cine'
            object_id = ObjectId(id)  # Convierte el ID proporcionado a un ObjectId
            result = collection.delete_one({'_id': object_id})  # Elimina un documento con el ID proporcionado

            # Si no se encuentra ninguna película con el ID dado, levanta una excepción 404
            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail=f"No se encontró ninguna película con el ID {id}")

            # Devuelve un mensaje de éxito si la película se elimina correctamente
            return {"message": f"Se eliminó correctamente la película con el ID {id}"}
        else:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
    except Exception as e:
        print(f'Error al eliminar el documento por ID: {e}')
        raise HTTPException(status_code=500, detail="Error al eliminar la película")


def create_film(film: Film):
    try:
        db = client()  # Llama a la función client() para obtener el cliente de MongoDB
        if db is not None:
            collection = db['films']  # Accede a la colección 'films' de la base de datos 'cine'

            # Convierte los datos del modelo Film en un diccionario para insertarlo en la base de datos
            film_dict = film.dict()

            # Inserta el nuevo documento en la colección
            result = collection.insert_one(film_dict)

            # Devuelve un mensaje de éxito si la película se agrega correctamente
            return {"message": "Película agregada correctamente", "film_id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
    except Exception as e:
        print(f'Error al crear la película: {e}')
        raise HTTPException(status_code=500, detail="Error al crear la película")


def update_film(id: str, film: Film):
    try:
        db = client()  # Llama a la función client() para obtener el cliente de MongoDB
        if db is not None:
            collection = db['films']  # Accede a la colección 'films' de la base de datos 'cine'
            object_id = ObjectId(id)  # Convierte el ID proporcionado a un ObjectId

            # Convierte los datos del modelo Film en un diccionario para actualizar el documento
            film_dict = film.dict(exclude_unset=True)  # Excluye los campos que no se han proporcionado

            # Realiza la actualización del documento en la base de datos
            result = collection.update_one({'_id': object_id}, {'$set': film_dict})

            # Verifica si se actualizó algún documento
            if result.modified_count == 0:
                raise HTTPException(status_code=404, detail=f"No se encontró ninguna película con el ID {id}")

            # Devuelve un mensaje de éxito si la película se actualiza correctamente
            return {"message": f"Se actualizó correctamente la película con el ID {id}"}
        else:
            raise HTTPException(status_code=500, detail="Error al conectar con la base de datos")
    except Exception as e:
        print(f'Error al actualizar la película: {e}')
        raise HTTPException(status_code=500, detail="Error al actualizar la película")
