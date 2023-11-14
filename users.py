from bson import ObjectId

class UserManager:
    def __init__(self, collection,articles_collection = None):
        self.users_collection = collection
        self.articles_collection = articles_collection

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

    def delete_user(self):
        print("Lista de Usuarios:")
        for user in self.users_collection.find():
            print(f"ID: {user['_id']}, Nombre: {user['name']}, Correo Electrónico: {user['email']}, Artículos: {user['articles']}, Comentarios: {user['comments']}")

        user_id = input("Ingresa el id del usuario a eliminar: ")

        #  # Convertir la cadena user_id a ObjectId
        user_id_object = ObjectId(user_id)

        # Eliminar el usuario y articulo
        result = self.users_collection.delete_one({"_id": user_id_object})
        delete_article = self.articles_collection.delete_many({"user_id":user_id})
        print("Articulos relacionados con el usuario han sido eliminados")