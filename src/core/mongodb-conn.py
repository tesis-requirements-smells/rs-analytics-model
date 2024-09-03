from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDBUtility:
    def __init__(self, uri, database_name):
        """Inicializa la conexión a MongoDB."""
        self.uri = uri
        self.database_name = database_name
        self.client = None
        self.db = None

    def connect(self):
        """Conecta a la base de datos MongoDB."""
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.database_name]
            print(f"Conectado a la base de datos: {self.database_name}")
        except ConnectionFailure as e:
            print(f"Error al conectar a MongoDB: {e}")

    def close(self):
        """Cierra la conexión a MongoDB."""
        if self.client:
            self.client.close()
            print("Conexión a MongoDB cerrada.")

    def insert_one(self, collection_name, document):
        """Inserta un documento en una colección."""
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        print(f"Documento insertado con ID: {result.inserted_id}")

    def find_one(self, collection_name, query):
        """Busca un documento en una colección."""
        collection = self.db[collection_name]
        result = collection.find_one(query)
        return result

    def update_one(self, collection_name, query, update):
        """Actualiza un documento en una colección."""
        collection = self.db[collection_name]
        result = collection.update_one(query, {"$set": update})
        print(f"Documentos actualizados: {result.modified_count}")

    def delete_one(self, collection_name, query):
        """Elimina un documento de una colección."""
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        print(f"Documentos eliminados: {result.deleted_count}")

