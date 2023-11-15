from bson import ObjectId

class UserManager:
    def __init__(self, collection,articles_collection = None,tags_collection = None,categories_collection = None,comments_collection = None):
        self.users_collection = collection
        self.articles_collection = articles_collection
        self.tags_collection = tags_collection
        self.categories_collection = categories_collection
        self.comments_collection = comments_collection

    def create_user(self):
        name = input("Ingrese el nombre del usuario: ")
        email = input("Ingrese el correo electrónico del usuario: ")

        new_user = {
            "name": name,
            "email": email,
            "articles": [],
            "comments": []
        }

        result = self.users_collection.insert_one(new_user)
        user_id = result.inserted_id

        print("Usuario creado:", user_id)

    def read_users(self):
        print("Lista de Usuarios:")
        for user in self.users_collection.find():
            print(f"ID: {user['_id']}, Nombre: {user['name']}, Correo Electrónico: {user['email']}, Artículos: {user['articles']}, Comentarios: {user['comments']}")


    def update_users(self):
        self.read_users()
        user_id = input("Ingrese el Id del usuario a actualizar:")
        name = input("Ingrese el nombre del usuario: ")
        email = input("Ingrese el correo electrónico del usuario: ")

        user_id_object = ObjectId(user_id)


        if name != '':
            self.users_collection.update_one({"_id": user_id_object}, {"$set": {"name": name}})
            print("Nombre actualizado correctamente",name)

        if email !='':
            self.users_collection.update_one({"_id": user_id_object}, {"$set": {"email": email}})
            print("Correo actualizado correctamente",email)
    
        self.articles_collection.update_many({"user_id":user_id},{"$set":{"user_name":name}})

    

    def delete_user(self):
        print("Lista de Usuarios:")
        for user in self.users_collection.find():
            print(f"ID: {user['_id']}, Nombre: {user['name']}, Correo Electrónico: {user['email']}, Artículos: {user['articles']}, Comentarios: {user['comments']}")

        user_id = input("Ingresa el id del usuario a eliminar: ")

        #  # Convertir la cadena user_id a ObjectId
        user_id_object = ObjectId(user_id)

        user = self.users_collection.find_one({"_id": user_id})

        article_ids = []
        for user in self.users_collection.find():
            for article_id in user["articles"]:
                article_ids.append(article_id)
                
        #print(article_ids)

        # Recorrer la colección de tags y eliminar los IDs de artículos asociados al usuario
        for tag in self.tags_collection.find():
            updated_urls =[]
            for url in tag["urls"]:
                if url not in article_ids:
                    updated_urls.append(url)
            self.tags_collection.update_one({"_id": tag["_id"]}, {"$set": {"urls": updated_urls}})

        # Recorrer la colección de categories y eliminar los IDs de artículos asociados al usuario
        for category in self.categories_collection.find():
            updated_urls =[]
            for url in category["urls"]:
                if url not in article_ids:
                    updated_urls.append(url)
            self.categories_collection.update_one({"_id": category["_id"]}, {"$set": {"urls": updated_urls}})
        

        #Eliminar los comentarios del usuario en la coleccion Comments 
        delete_comments =self.comments_collection.delete_many({"usuario_id":user})


        # Eliminar el usuario 
        result = self.users_collection.delete_one({"_id": user_id_object})
        #Elimina el articulo asociado al usuario
        delete_article = self.articles_collection.delete_many({"user_id":user_id})

        print("EL usuario y sus articulos relacionados han sido eliminados")

    
    def delete_user_comment(self,id):
        
        for user in self.users_collection.find():
            for comment in user["comments"]:
                if comment == id:
                    commentList = user["comments"]
                    index = commentList.index(comment)
                    print(index)
                    commentList.pop(index)

                    self.users_collection.update_one({"_id": user["_id"]}, {"$set": {"comments": commentList}})


