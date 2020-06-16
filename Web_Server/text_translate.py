import os
import json
import pymongo
from google.cloud import translate_v2
from textblob import TextBlob
import re
import pprint

cadena_de_conexion = "mongodb+srv://dbJoseZamora:balto1010@gbd2020-uzfjc.mongodb.net/gbd2020?retryWrites=true&w=majority"
gbd2020_Cluster=pymongo.MongoClient(cadena_de_conexion)
DB_TweetsPrueba = gbd2020_Cluster.tweetsPrueba
Coll_TweetsNew = DB_TweetsPrueba.tweetsCorrupcion

Query = Coll_TweetsNew.find()


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"F:\Google_Drive\ESPE\Sexto_Semestre\Gestion_de_Base_de_Datos_Estevan_Gomez_6199\Parcial1\Trabajos_en_Grupo\Proyecto\Web_Server\gckey.json"

translate_client = translate_v2.Client()

for tweet in Query:
    text = tweet.get('text')
    text = text.lower()
    cleanString = re.sub(r"[^ \nA-Za-z0-9À-ÖØ-öø-ÿ/]+",' ', text)
    target = 'en'
    output = translate_client.translate(
        cleanString,
        target_language = target
    )
    text = output['translatedText']
    print(text)
    blob = TextBlob(text)
    sentimen = blob.sentiment.polarity
    newvalues = {"$set":{"text": text,"sentiment":sentimen}}
    Coll_TweetsNew.update_one({'_id':tweet.get('_id')},newvalues)











