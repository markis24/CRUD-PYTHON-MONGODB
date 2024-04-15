from pymongo import MongoClient


def client():
    try:
        # URL de conexión a MongoDB
        server = "mongodb://localhost:27017/"

        # Intentamos conectarnos a MongoDB y devolvemos la base de datos 'cine' si la conexión es exitosa
        mongo_client = MongoClient(server)
        db = mongo_client.cine  # Acceder a la base de datos 'cine'
        return db

    except Exception as e:
        # Si hay algún error, capturamos la excepción específica de pymongo y la imprimimos
        print(f'Error al conectarse a MongoDB: {e}')
        return None  # Devolvemos None si hay un error
