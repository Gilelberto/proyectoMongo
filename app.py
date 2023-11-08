import initDb
#instalar 
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["blogDB"]

initDb.initDb(mydb)

print(myclient.list_database_names())


