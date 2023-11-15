from bson import ObjectId

class TagManager:
    def __init__(self, tags_collection, articles_collection,mydb,article_manager=None):
        self.tags_collection = tags_collection
        self.articles_collection = articles_collection
        self.mydb = mydb
        self.article_manager = article_manager

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

    def update_tag(self):
        # Mostrar todos los tags disponibles
        print("Lista de Tags:")
        for tag in self.tags_collection.find():
            print(f"ID: {tag['_id']}, Nombre: {tag['name']}")

        tag_id = input("Ingrese el ID del tag que desea actualizar: ")

        # Verificar si el tag existe
        tag = self.tags_collection.find_one({"_id": ObjectId(tag_id)})
        if not tag:
            print("Tag no encontrado.")
            return

        # Obtener valores actuales del tag
        current_name = tag['name']

        # Solicitar al usuario los nuevos valores o dejar los actuales si no se proporcionan
        new_name = input(f"Ingrese el nuevo nombre del tag (actual: {current_name}): ") or current_name

        # Actualizar el tag
        self.tags_collection.update_one({"_id": ObjectId(tag_id)}, {"$set": {"name": new_name}})

        print(f"Tag actualizado con ID: {tag_id}")


    def read_tags(self):
        for tag in self.tags_collection.find():
            print(f"ID: {tag['_id']}, Nombre: {tag['name']}, Url: {tag['urls']}")


    def delete_tag(self):
        print("Lista de Tags:")
        for tag in self.tags_collection.find():
            print(f"ID: {tag['_id']},Nombre:{tag['name']}, Url: {tag['urls']}]")

        tag_id = input("Ingresa el id de el tag a eliminar: ")

        # Convertir la cadena tag_id a ObjectId
        tag_id_object = ObjectId(tag_id)
        #Eliminar el id_tag en el articulo
        self.article_manager.delete_article_tag(self,tag_id_object)
        # Eliminar el tag
        result = self.tags_collection.delete_one({"_id": tag_id_object})
        print("Tag ELiminado Correctamente")
            

    





