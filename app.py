
import users
import articles
#instalar 
import pymongo
import os


myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["blogDB"]

users_collection = mydb["users"]
articles_collection = mydb["articles"]


print(myclient.list_database_names())



def handle_create_option(opcion2):
    print("*CREAR*")
    if opcion2 == '1':
        users.get_and_create_user(users_collection)
    elif opcion2 == '2':
        articles.get_and_create_article(articles_collection)
    elif opcion2 == '3':
        print("Crear comentario")
    elif opcion2 == '4':
        print("Crear tag")
    elif opcion2 == '5':
        print("Crear categoría")
    else:
        print("Opción no válida en el segundo submenu")

def handle_read_option(opcion2):
    print("LEER")
    if opcion2 == '1':
        users_list = users.read_users(users_collection)
        print("Usuarios:",users_list)
    elif opcion2 == '2':
        articles_list = articles.read_articles(articles_collection)
        print("Articles:",articles_list)
    elif opcion2 == '3':
        print("Leer comentario")
    elif opcion2 == '4':
        print("Leer tag")
    elif opcion2 == '5':
        print("Leer categoría")
    else:
        print("Opción no válida en el segundo submenu")

def handle_update_option(opcion2):
    print("ACTUALIZAR")
    if opcion2 == '1':
        user_id = input("Ingrese el ID del usuario que desea actualizar: ")
        users.update_user(users_collection, user_id)
    elif opcion2 == '2':
        article_id = input("Ingrese el ID del articulo que desea actualizar:")
        articles.update_article(articles_collection,article_id)
    elif opcion2 == '3':
        print("Actualizar comentario")
    elif opcion2 == '4':
        print("Actualizar tag")
    elif opcion2 == '5':
        print("Actualizar categoría")
    else:
        print("Opción no válida en el segundo submenu")

def handle_delete_option(opcion2):
    print("ELIMINAR")
    if opcion2 == '1':
        user_id = input("Ingrese el ID del usuario que desea eliminar: ")
        users.delete_user(users_collection, user_id)
    elif opcion2 == '2':
        article_id = input("Ingrese el ID del articulo que desea eliminar: ")
        articles.delete_article(articles_collection, article_id)
    elif opcion2 == '3':
        print("Eliminar comentario")
    elif opcion2 == '4':
        print("Eliminar tag")
    elif opcion2 == '5':
        print("Eliminar categoría")
    else:
        print("Opción no válida en el segundo submenu")

while True:

    os.system('cls' if os.name == 'nt' else 'clear')
    print("--Menu---")
    print("1. Crear")
    print("2. Leer")
    print("3. Actualizar")
    print("4. Eliminar")
    print("5. Salir")
    opcion1 = input("Ingrese una opcion:")

    if opcion1 == '5':
        break
    


    while True:
        print("--Submenu--")
        print("1. Usuario")
        print("2. Articulo")
        print("3. Comentario")
        print("4. Tag")
        print("5. Categorias")
        print("6. Salir")
        opcion2 = input("Ingrese una opcion:")

        if opcion2 == '6':
            break

        if opcion1 == '1':
            handle_create_option(opcion2)
        elif opcion1 == '2':
            handle_read_option(opcion2)
        elif opcion1 == '3':
            handle_update_option(opcion2)
        elif opcion1 == '4':
            handle_delete_option(opcion2)
        else:
            print("Opción no válida en el primer menu")
            break

    













