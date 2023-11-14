from bson import ObjectId
import os
import pymongo
from users import UserManager
from articles import ArticleManager
from tags import TagManager
from categories import CategoryManager

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["blogDB"]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


users_manager = UserManager(mydb["users"])
articles_manager = ArticleManager(mydb["articles"], mydb["users"], mydb["tags"], mydb["categories"])
tags_manager = TagManager(mydb["tags"], mydb["articles"])
categories_manager = CategoryManager(mydb["categories"], mydb["articles"])


while True:
    clear_screen()
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
            if opcion2 == '1':
                users_manager.create_user()
            elif opcion2 == '2':
                articles_manager.get_and_create_article()
            elif opcion2 == '3':
                print("Crear comentario")
            elif opcion2 == '4':
                tags_manager.get_and_create_tag()
            elif opcion2 == '5':
                categories_manager.create_category()
            else:
                print("Opción no válida en el segundo submenu")

        elif opcion1 == '2':
            if opcion2 == '1':
                users_manager.read_users()
            elif opcion2 == '2':
                articles_manager.read_articles()
            elif opcion2 == '3':
                print("Leer comentario")
            elif opcion2 == '4':
                print("Leer tag")
            elif opcion2 == '5':
                print("Leer categoría")
            else:
                print("Opción no válida en el segundo submenu")

        elif opcion1 == '3':
            if opcion2 == '1':
                print("actualizar usuario")
            elif opcion2 == '2':
                print("actualizar articulo")
            elif opcion2 == '3':
                print("Actualizar comentario")
            elif opcion2 == '4':
                print("Actualizar tag")
            elif opcion2 == '5':
                print("Actualizar categoría")
            else:
                print("Opción no válida en el segundo submenu")

        elif opcion1 == '4':
            if opcion2 == '1':
                print("eliminar usuario")
            elif opcion2 == '2':
                print("eliminar articulo")
            elif opcion2 == '3':
                print("Eliminar comentario")
            elif opcion2 == '4':
                print("Eliminar tag")
            elif opcion2 == '5':
                print("Eliminar categoría")
            else:
                print("Opción no válida en el segundo submenu")
