from bson import ObjectId

class CategoryManager:
    def __init__(self, categories_collection, articles_collection):
        self.categories_collection = categories_collection
        self.articles_collection = articles_collection

    def create_category(self):
        nombre_categoria = input("Ingrese el nombre de la categoría: ")

        # Mostrar todos los artículos disponibles para asociar
        print("Lista de Artículos disponibles para asociar a la categoría:\n")
        articles = self.articles_collection.find()
        for article in articles:
            print(f"ID: {article['_id']}, Título: {article['title']}")

        # Pedir al usuario que introduzca los IDs de los artículos, separados por comas
        articulos_input = input("Ingrese los IDs de los artículos asociados a la categoría, separados por comas (deje en blanco si no desea asociar artículos): ")

        # Convertir la cadena de IDs en una lista, y crear ObjectIds válidos para MongoDB
        articulos_ids = [ObjectId(x.strip()) for x in articulos_input.split(",") if x.strip()] if articulos_input else []

        # Crear el documento categoría
        categoria_data = {"name": nombre_categoria, "urls": articulos_ids}
        result = self.categories_collection.insert_one(categoria_data)

        # Si se proporcionaron artículos, actualizar sus documentos para añadir esta categoría
        if articulos_ids:
            for articulo_id in articulos_ids:
                self.articles_collection.update_one({"_id": articulo_id}, {"$push": {"categories": result.inserted_id}})

        print(f"Categoría creada con ID: {result.inserted_id}")

    def read_category(self):
        for category in self.categories_collection.find():
            print(f"ID: {category['_id']}, Nombre: {category['name']}, Url: {category['urls']}")
            
