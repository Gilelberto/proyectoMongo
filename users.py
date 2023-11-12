from bson import ObjectId

def get_and_create_user(users_collection):
    #users_collection = mydb["users"]

    name = input("Ingrese el nombre del usuario: ")
    email = input("Ingrese el correo electrónico del usuario: ")

    new_user = {
        "name": name,
        "email": email,
        "articlesList": [],
        "commentsList": []
    }

    result = users_collection.insert_one(new_user)
    user_id = result.inserted_id

    print("Usuario creado:", user_id)
    return user_id


def read_users(users_collection):
    users = users_collection.find()
    return list(users)




def update_user(users_collection, user_id):
    # Convertir la cadena user_id a ObjectId
    user_id_object = ObjectId(user_id)
    existing_user = users_collection.find_one({"_id": user_id_object})

    if existing_user:
        print("Usuario encontrado. Puedes proceder con la actualización.")

        while True:
            print("¿Qué atributo deseas actualizar?")
            print("1. Nombre")
            print("2. Correo Electrónico")
            print("3. Salir")

            option = input("Ingrese la opción: ")

            if option == '1':
                new_name = input("Ingrese el nuevo nombre del usuario: ")
                users_collection.update_one({"_id": user_id_object}, {"$set": {"name": new_name}})
                print("Nombre actualizado exitosamente.")
            elif option == '2':
                new_email = input("Ingrese el nuevo correo electrónico del usuario: ")
                users_collection.update_one({"_id": user_id_object}, {"$set": {"email": new_email}})
                print("Correo electrónico actualizado exitosamente.")
            elif option == '3':
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")
    else:
        print("No se encontró un usuario con el ID proporcionado.")



def delete_user(users_collection, user_id):
    #users_collection = mydb["users"]
    # Convertir la cadena user_id a ObjectId
    user_id_object = ObjectId(user_id)

    existing_user = users_collection.find_one({"_id": user_id_object})


    if existing_user:
        users_collection.delete_one({"_id": user_id_object})
        print("Usuario eliminado")
    else:
        print("Usuario Inexistente")


    

