import json
import io
import os
import pymongo
#Conexion con la base de datos

cadena_de_conexion = "mongodb+srv://dbJoseZamora:balto1010@gbd2020-uzfjc.mongodb.net/gbd2020?retryWrites=true&w=majority"

gbd2020_Cluster=pymongo.MongoClient(cadena_de_conexion)

DB_TweetsPrueba = gbd2020_Cluster.tweetsPrueba
Coll_TweetsNew = DB_TweetsPrueba.tweetsNew

#Apertura del archivo que va a contener las coordenadas
print(os.path.exists("coordenadas.tweets.txt"))
if os.path.exists("coordenadas.tweets.txt"):
    os.remove("coordenadas.tweets.txt")
coords_file = io.open('coordenadas.tweets.txt','a',encoding="utf-8")
#Query de los datos desde la base de datos
Query = Coll_TweetsNew.find({'$and': [{'geoLocation.coordinates.0':{'$lte': -78.399068,'$gte': -78.630747}},{'geoLocation.coordinates.1':{'$lte':0.009190,'$gte':-0.393909}}]})
#Separacion de las coordenadas de cada Tweet
for tweet in Query:
    coordinates = tweet.get("geoLocation").get("coordinates")
    latitud = str(coordinates[1])
    longitud = str(coordinates[0])
    coordinate = latitud+" "+longitud
    coords_file.write(coordinate+"\n")
    print(coordinate)
coords_file.close()