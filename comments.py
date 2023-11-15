from bson import ObjectId
from articles import ArticleManager
from users import UserManager

class CommentManager:
    def __init__(self, comments_collection,users_collection,articles_collection,mydb,article_manager = None,user_manager = None):
        self.comments_collection = comments_collection
        self.users_collection = users_collection
        self.articles_collection = articles_collection
        self.mydb = mydb
        self.article_manager = article_manager
        self.user_manager = user_manager

    def get_and_create_comment(self):
        users_manager = UserManager(self.users_collection)
        articles_manager = ArticleManager(self.articles_collection,self.mydb["users"],self.mydb["tags"],self.mydb["categories"],self.mydb["comments"])

        users_manager.read_users()
        usuario_id= input("Ingrese el ID del usuario que va a comentar: ")
        
        articles_manager.read_articles()
        article_id = input("Ingrese el ID del articulo que va a comentar: ")

        name_comment = input("Ingrese el comentario: ")
        
        new_comment ={
            "usuario_id":usuario_id,
            "name":name_comment,
            "url":article_id
        }

        result = self.comments_collection.insert_one(new_comment)
        comment_id = result.inserted_id

        print("Comentario",comment_id)

        # Actualizar el usuario 
        self.users_collection.update_one({"_id": ObjectId(usuario_id)}, {"$push": {"comments": comment_id}})

        self.articles_collection.update_one({"_id": ObjectId(article_id)}, {"$push": {"comments": comment_id}})


    def read_comments(self):
        print("Lista de Comentarios:")
        for comment in self.comments_collection.find():
            print(f"ID: {comment['_id']},Usuario_id:{comment['usuario_id']},Nombre: {comment['name']}, Url: {comment['url']}]")

    def update_comment(self):
        self.read_comments()
        comment_id = input("Ingrese el ID del comentario que desea actualizar: ")

        # Verificar si el comentario existe
        comment = self.comments_collection.find_one({"_id": ObjectId(comment_id)})
        if not comment:
            print("Comentario no encontrado.")
            return

        # Obtener el valor actual del comentario
        current_name = comment['name']

        # Solicitar al usuario el nuevo valor o dejar el actual si no se proporciona
        new_name = input(f"Ingrese el nuevo nombre del comentario (actual: {current_name}): ") or current_name

        # Actualizar el comentario en la colección
        self.comments_collection.update_one({"_id": ObjectId(comment_id)}, {"$set": {"name": new_name}})

        print("Comentario actualizado correctamente.")


    def delete_comment(self):
        print("Lista de Comentarios:")
        for comment in self.comments_collection.find():
            print(f"ID: {comment['_id']},Usuario_id:{comment['usuario_id']},Nombre: {comment['name']}, Url: {comment['url']}]")

        comment_id = input("Ingresa el id del comentario a eliminar: ")

        # Convertir la cadena user_id a ObjectId
        comment_id_object = ObjectId(comment_id)
        #eliminar comentarios en articulos
        self.article_manager.delete_article_comment(self,comment_id_object)
        #eliminar comentarios en user
        self.user_manager.delete_user_comment(self,comment_id_object)
        # Eliminar el comentario
        result = self.comments_collection.delete_one({"_id": comment_id_object})
        print("Comentario ELiminado Correctamente")




    


