from bson import ObjectId

def get_and_create_article(articles_collection):
    title = input("Ingrese el titulo del articulo: ")
    date = input("Ingrese la fecha del articulo: ")
    text = input("Ingrese el texto del articulo: ")


    new_article = {
        "title": title,
        "date": date,
        "text": text,
        "commentsList":[],
        "tagsList":[],
        "categoriesList":[]
    }

    result = articles_collection.insert_one(new_article)
    article_id = result.inserted_id

    print("Articulo Creado:", article_id)
    return article_id


def read_articles(articles_collection):
    articles = articles_collection.find()
    return list(articles)



def update_article(articles_collection, article_id):
    # Convertir la cadena article_id a ObjectId
    article_id_object = ObjectId(article_id)
    existing_article = articles_collection.find_one({"_id": article_id_object})

    if existing_article:
        print("Articulo encontrado. Puedes proceder con la actualización.")

        while True:
            print("¿Qué atributo deseas actualizar?")
            print("1. Título")
            print("2. Fecha")
            print("3. Texto")
            print("4. Salir")

            option = input("Ingrese la opción: ")

            if option == '1':
                new_title = input("Ingrese el nuevo título del artículo: ")
                articles_collection.update_one({"_id": article_id_object}, {"$set": {"title": new_title}})
                print("Título actualizado exitosamente.")
            elif option == '2':
                new_date = input("Ingrese la nueva fecha del artículo: ")
                articles_collection.update_one({"_id": article_id_object}, {"$set": {"date": new_date}})
                print("Fecha actualizada exitosamente.")
            elif option == '3':
                new_text = input("Ingrese el nuevo texto del artículo: ")
                articles_collection.update_one({"_id": article_id_object}, {"$set": {"text": new_text}})
                print("Texto actualizado exitosamente.")
            elif option == '4':
                print("Saliendo...")
                break
            else:
                print("Opción no válida.")
    else:
        print("No se encontró un artículo con el ID proporcionado.")




def delete_article(articles_collection,article_id):
    # Convertir la cadena article_id a ObjectId
    article_id_object = ObjectId(article_id)
    existing_article = articles_collection.find_one({"_id": article_id_object})

    if existing_article:
        articles_collection.delete_one({"_id": article_id_object})
        print("Articulo eliminado")
    else:
        print("Articulo Inexistente")