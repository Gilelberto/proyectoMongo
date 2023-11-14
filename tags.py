from bson import ObjectId

class TagManager:
    def __init__(self, tags_collection, articles_collection):
        self.tags_collection = tags_collection
        self.articles_collection = articles_collection

    def get_and_create_tag(self):
        nombre_tag = input("Ingrese el nombre del tag: ")
        
        # Mostrar todos los artículos disponibles para asociar
        print("Lista de Artículos disponibles para asociar al tag:\n")
        for article in self.articles_collection.find():
            print(f"ID: {article['_id']}, Título: {article['title']}")

        # Pedir al usuario que introduzca los IDs de los artículos, separados por comas
        articulos_input = input("Ingrese los IDs de los artículos asociados al tag, separados por comas (deje en blanco si no desea asociar artículos): ")
        
        # Convertir la cadena de IDs en una lista, y crear ObjectIds válidos para MongoDB
        articulos_ids = [ObjectId(x.strip()) for x in articulos_input.split(",") if x.strip()] if articulos_input else []

        # Crear el documento tag
        tag_data = {"name": nombre_tag, "urls": articulos_ids}
        result = self.tags_collection.insert_one(tag_data)
        
        # Si se proporcionaron artículos, actualizar sus documentos para añadir este tag
        if articulos_ids:
            for articulo_id in articulos_ids:
                self.articles_collection.update_one({"_id": articulo_id}, {"$push": {"tags": result.inserted_id}})
        
        print(f"Tag creado con ID: {result.inserted_id}")
        return result.inserted_id


    def read_tags(self):
        for tag in self.tags_collection.find():
            print(f"ID: {tag['_id']}, Nombre: {tag['name']}, Url: {tag['urls']}")





