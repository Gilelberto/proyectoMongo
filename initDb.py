def initDb(mydb):
    #users
    mycol = mydb["users"]
    newUser = {"name": "Jessanahil", "email":"a358509@guash.mx" }
    mycol.insert_one(newUser)

    #articles
    mycol = mydb["articles"]
    newArticle = {"title": "Como superar una reprobada de De Lira", "date":"17/11/2023" , "text": "1.-Mime\n2.-Suicidiop." }
    x = mycol.insert_one(newArticle)
    x.inserted_id

    #comments
    mycol = mydb["comments"]
    newComment = {"name": "Pedrito Sola", "url":x}
    mycol.insert_one(newComment)

    #tags
    mycol = mydb["tags"]
    newTag = {"name": "Pedrito Sola", "url":x}
    mycol.insert_one(newTag)

    #categories
    mycol = mydb["categories"]
    newCategorie = {"name": "Pedrito Sola", "url":x}
    mycol.insert_one(newCategorie)