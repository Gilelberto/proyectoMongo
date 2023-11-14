from bson import ObjectId

class ArticleManager:
    def __init__(self, articles_collection, users_collection, tags_collection, categories_collection):
        self.articles_collection = articles_collection
        self.users_collection = users_collection
        self.tags_collection = tags_collection
        self.categories_collection = categories_collection

    def get_and_create_article(self):
        print("Lista de Usuarios:")
        for user in self.users_collection.find():
            print(f"ID: {user['_id']}, Nombre: {user['name']}, Correo: {user['email']}")

        usuario_id = input("Ingrese el ID del usuario al que desea asociar el artículo: ")
        usuario = self.users_collection.find_one({"_id": ObjectId(usuario_id)})
        nombre_usuario = usuario["name"] if usuario else "Usuario Desconocido"

        titulo = input("Ingrese el título del artículo: ")
        fecha = input("Ingrese la fecha del artículo (formato YYYY-MM-DD): ")
        contenido = input("Ingrese el contenido del artículo: ")

        # Pedir tags al usuario
        tags_input = input("Ingrese los nombres de los tags, separados por comas (si no existen se crearán): ")
        tags_nombres = [x.strip() for x in tags_input.split(",") if x.strip()]

        # Inicializar la lista de ObjectIds de tags para el artículo
        tags_ids = []

        # Verificar si cada tag ya existe, si no, crearlo
        for nombre_tag in tags_nombres:
            tag = self.tags_collection.find_one({"name": nombre_tag})
            if tag:
                tags_ids.append(tag['_id'])
            else:
                nuevo_tag = {"name": nombre_tag, "urls": []}
                tag_result = self.tags_collection.insert_one(nuevo_tag)
                tags_ids.append(tag_result.inserted_id)
                print(f"Tag creado con ID: {tag_result.inserted_id} y nombre {nombre_tag}")

        # Pedir categorías al usuario
        categorias_input = input("Ingrese los nombres de las categorías, separados por comas (si no existen se crearán): ")
        categorias_nombres = [x.strip() for x in categorias_input.split(",") if x.strip()]

        # Inicializar la lista de ObjectIds de categorías para el artículo
        categorias_ids = []

        # Verificar si cada categoría ya existe, si no, crearlo
        for nombre_categoria in categorias_nombres:
            categoria = self.categories_collection.find_one({"name": nombre_categoria})
            if categoria:
                categorias_ids.append(categoria['_id'])
            else:
                nueva_categoria = {"name": nombre_categoria, "urls": []}
                categoria_result = self.categories_collection.insert_one(nueva_categoria)
                categorias_ids.append(categoria_result.inserted_id)
                print(f"Categoría creada con ID: {categoria_result.inserted_id} y nombre {nombre_categoria}")

        # Crear el artículo con los tags y categorías asociadas
        article_data = {
            "title": titulo,
            "date": fecha,
            "text": contenido,
            "user_id": usuario_id,
            "user_name": nombre_usuario,
            "comments": [],
            "tags": tags_ids,
            "categories": categorias_ids
        }
        article_result = self.articles_collection.insert_one(article_data)

        # Actualizar la colección de tags y categorías para incluir la URL del nuevo artículo
        for tag_id in tags_ids:
            self.tags_collection.update_one({"_id": tag_id}, {"$push": {"urls": article_result.inserted_id}})
        for categoria_id in categorias_ids:
            self.categories_collection.update_one({"_id": categoria_id}, {"$push": {"urls": article_result.inserted_id}})

        # Actualizar el usuario con el nuevo artículo
        self.users_collection.update_one({"_id": ObjectId(usuario_id)}, {"$push": {"articles": article_result.inserted_id}})

        print(f"Artículo creado con ID: {article_result.inserted_id}")

    def read_articles(self):
        print("Lista de Artículos:")
        print("\n")
        for article in self.articles_collection.find():
            print(f"ID: {article['_id']}, Título: {article['title']}, Fecha: {article['date']}, Usuario: {article['user_name']}")
            print("Contenido:")
            print(article['text'])
            print("Tags:")
            for tag_id in article['tags']:
                tag = self.tags_collection.find_one({"_id": tag_id})
                print(f"  - {tag['name']}")
            print("Categorías:")
            for category_id in article['categories']:
                category = self.categories_collection.find_one({"_id": category_id})
                print(f"  - {category['name']}")
            print("Comentarios:")
            for comment in article['comments']:
                print(f"  - {comment}")
            print("\n")


