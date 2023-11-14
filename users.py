from bson import ObjectId

class UserManager:
    def __init__(self, collection):
        self.users_collection = collection

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
