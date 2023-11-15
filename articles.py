from bson import ObjectId

class ArticleManager:
    def __init__(self, articles_collection, users_collection, tags_collection, categories_collection,comments_collection):
        self.articles_collection = articles_collection
        self.users_collection = users_collection
        self.tags_collection = tags_collection
        self.categories_collection = categories_collection
        self.comments_collection = comments_collection

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



    def update_article(self):
        print("Lista de Artículos:")
        for article in self.articles_collection.find():
            print(f"ID: {article['_id']}, Título: {article['title']}")

        article_id = input("Ingrese el ID del artículo que desea actualizar: ")

        # Verificar si el artículo existe
        article = self.articles_collection.find_one({"_id": ObjectId(article_id)})
        if not article:
            print("Artículo no encontrado.")
            return

        # Obtener valores actuales del artículo
        current_title = article['title']
        current_date = article['date']
        current_text = article['text']

        # Solicitar al usuario los nuevos valores o dejar los actuales si no se proporcionan
        new_title = input(f"Ingrese el nuevo título del artículo (actual: {current_title}): ") or current_title
        new_date = input(f"Ingrese la nueva fecha del artículo (actual: {current_date}): ") or current_date
        new_text = input(f"Ingrese el nuevo contenido del artículo (actual: {current_text}): ") or current_text

        # Actualizar tags si se proporcionan nuevos valores
        new_tags_input = input("Ingrese los nombres de los nuevos tags, separados por comas (si no existen se crearán): ")
        new_tags_names = [x.strip() for x in new_tags_input.split(",") if x.strip()]
        new_tags_ids = []

        # Verificar si updated_data ya está inicializado
        if 'updated_data' not in locals():
            updated_data = {}

        for tag_name in new_tags_names:
            tag = self.tags_collection.find_one({"name": tag_name})
            if tag:
                new_tags_ids.append(tag['_id'])
            else:
                new_tag = {"name": tag_name, "urls": [ObjectId(article_id)]}
                tag_result = self.tags_collection.insert_one(new_tag)
                new_tags_ids.append(tag_result.inserted_id)
                print(f"Tag creado con ID: {tag_result.inserted_id} y nombre {tag_name}")

        updated_data["tags"] = new_tags_ids

        # Actualizar categorías si se proporcionan nuevos valores
        new_categories_input = input("Ingrese los nombres de las nuevas categorías, separadas por comas (si no existen se crearán): ")
        new_categories_names = [x.strip() for x in new_categories_input.split(",") if x.strip()]
        new_categories_ids = []

        for category_name in new_categories_names:
            category = self.categories_collection.find_one({"name": category_name})
            if category:
                new_categories_ids.append(category['_id'])
            else:
                new_category = {"name": category_name, "urls": [ObjectId(article_id)]}
                category_result = self.categories_collection.insert_one(new_category)
                new_categories_ids.append(category_result.inserted_id)
                print(f"Categoría creada con ID: {category_result.inserted_id} y nombre {category_name}")

        updated_data["categories"] = new_categories_ids

        # Resto del código para actualizar el artículo...
        # Actualizar el artículo en la colección
        self.articles_collection.update_one({"_id": ObjectId(article_id)}, {"$set": updated_data})

        # Actualizar las tags y categorías para incluir la nueva URL del artículo
        for tag_id in new_tags_ids:
            self.tags_collection.update_one({"_id": tag_id}, {"$push": {"urls": ObjectId(article_id)}})

        for category_id in new_categories_ids:
            self.categories_collection.update_one({"_id": category_id}, {"$push": {"urls": ObjectId(article_id)}})

        print("Artículo actualizado correctamente.")


            
    def delete_article_comment(self,id):

        for article in self.articles_collection.find():
            #print(article["comments"])
            for comment in article["comments"]:
                if comment  == id:
                    commentList = article["comments"]
                    index = commentList.index(comment)
                    print(index)
                    commentList.pop(index)
    
                    self.articles_collection.update_one({"_id": article["_id"]}, {"$set": {"comments": commentList}})


    def delete_article_category(self,id):

        for article in self.articles_collection.find():
            #print(article["categories"])
            for category in article["categories"]:
                if category  == id:
                    categoryList = article["categories"]
                    index = categoryList.index(category)
                    print(index)
                    categoryList.pop(index)
    
                    self.articles_collection.update_one({"_id": article["_id"]}, {"$set": {"categories": categoryList}})



    def delete_article_tag(self,id):

        for article in self.articles_collection.find():
            #print(article["tags"])
            for tag in article["tags"]:
                if tag  == id:
                    tagList = article["tags"]
                    index = tagList.index(tag)
                    print(index)
                    tagList.pop(index)
    
                    self.articles_collection.update_one({"_id": article["_id"]}, {"$set": {"tags": tagList}})
        

    def delete_article(self):

        self.read_articles()
        article_id = input("Ingresa el Id del articulo a eliminar: ")

        # Convertir la cadena user_id a ObjectId
        article_id_object = ObjectId(article_id)
        article = self.articles_collection.find_one({"_id": article_id_object})

        user_id = article["user_id"]
        user_id_object = ObjectId(user_id)

        #eliminar el articuloid de la lista de articulos en usuario 
        self.users_collection.update_one({"_id": user_id_object},{"$pull": {"articles": article_id_object}})

        #eliminar el commentid de la lista de comentarios en usuario

        comment_ids = []
        for comment_id in article["comments"]:
            comment_ids.append(comment_id)

        for comment_id in comment_ids:
            self.users_collection.update_one({"_id": user_id_object}, {"$pull": {"comments": comment_id}})

        # Eliminar el artículo de la lista de URLs de los TAGS asociados
        for tag_id in article["tags"]:
            self.tags_collection.update_one({"_id": tag_id},{"$pull": {"urls": article_id_object}})

        # Eliminar el artículo de la lista de URLs de las CATEGORIAS asociadas
        for category_id in article["categories"]:
            self.categories_collection.update_one({"_id": category_id},{"$pull": {"urls": article_id_object}})

        #Eliminar los comentarios que esten asociados al article id especificado 
        self.comments_collection.delete_many({"url": article_id})


        #Eliminar el articulo 
        self.articles_collection.delete_many({"_id": article_id_object})



        
        


        











