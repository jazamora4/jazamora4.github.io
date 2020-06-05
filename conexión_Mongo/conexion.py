import pymongo

cliente_mongoDB = pymongo.MongoClient(
    "mongodb+srv://dbJoseZamora:balto1010@gbd2020-uzfjc.mongodb.net/gbd2020?retryWrites=true&w=majority")

baseDeDatos = cliente_mongoDB.test
coleccion = baseDeDatos.foods

coleccion.delete_many({
    "calories": {
        "$lt": 300
    }
})


 
